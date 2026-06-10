"""
Offline tests for the SFP CL-Bench bridge system.

These exercise the adapter's logic — structured-output extraction, the
schema-validation/repair loop, experiential ``observe`` accumulation, and
``reset`` — without a GPU or any model download. We stand up a minimal stub of
CL-Bench's ``src`` package so the real relative imports in ``system.py``
resolve, then monkeypatch model loading and generation.

Run:
    python clbench/test_sfp_system.py
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
import tempfile
import textwrap
from types import ModuleType

from pydantic import BaseModel


def _build_stub_clbench(tmp: str) -> str:
    """Create a fake ``src`` package with the interface/registry/usage symbols
    that ``sfp_system.system`` imports, plus the bundled adapter at
    ``src/systems/sfp``. Returns the directory to put on ``sys.path``."""
    src = os.path.join(tmp, "src")
    os.makedirs(os.path.join(src, "systems"), exist_ok=True)
    open(os.path.join(src, "__init__.py"), "w").close()
    open(os.path.join(src, "systems", "__init__.py"), "w").close()

    with open(os.path.join(src, "interface.py"), "w") as f:
        f.write(
            textwrap.dedent(
                '''
                from dataclasses import dataclass, field
                from typing import Any, Optional
                from pydantic import BaseModel

                @dataclass
                class Observation:
                    content: str
                    instance_complete: bool = True
                    metadata: Optional[dict] = None

                @dataclass
                class Query:
                    prompt: str
                    response_schema: type
                    feedback: Optional[Observation] = None
                    instance_id: Optional[str] = None
                    instance_index: Optional[int] = None
                    metadata: Optional[dict] = None

                @dataclass
                class Response:
                    action: BaseModel
                    metadata: Optional[dict] = None

                class ContinualLearningSystem:
                    parallel_safe = True
                    def record_usage_event(self, e):
                        # Lazy init: subclasses (like SFPSystem) don't call super().__init__.
                        if not hasattr(self, "_usage"):
                            self._usage = []
                        self._usage.append(e)
                    def consume_usage_events(self):
                        out = getattr(self, "_usage", [])
                        self._usage = []
                        return out
                    def observe(self, observation, next_query=None):
                        pass
                    def get_run_artifacts(self):
                        return None
                '''
            )
        )
    with open(os.path.join(src, "registry.py"), "w") as f:
        f.write(
            textwrap.dedent(
                """
                SYSTEMS_REGISTRY = {}
                def register_system(name):
                    def deco(cls):
                        SYSTEMS_REGISTRY[name] = cls
                        return cls
                    return deco
                """
            )
        )
    with open(os.path.join(src, "usage.py"), "w") as f:
        f.write(
            textwrap.dedent(
                """
                from dataclasses import dataclass
                from typing import Optional
                @dataclass
                class UsageEvent:
                    call_type: str
                    model: str
                    provider: Optional[str] = None
                    input_tokens: Optional[int] = None
                    output_tokens: Optional[int] = None
                    total_tokens: Optional[int] = None
                    cost_usd: Optional[float] = None
                    pricing_source: Optional[str] = None
                """
            )
        )

    # Drop the real adapter package into src/systems/sfp.
    here = os.path.dirname(os.path.abspath(__file__))
    import shutil

    shutil.copytree(
        os.path.join(here, "sfp_system"), os.path.join(src, "systems", "sfp")
    )
    return tmp


class PokerAction(BaseModel):
    move: str
    amount: int = 0


def _load_system_class(tmp_root: str):
    sys.path.insert(0, tmp_root)
    # Ensure a clean import of our stub 'src'.
    for mod in [m for m in sys.modules if m == "src" or m.startswith("src.")]:
        del sys.modules[mod]
    module = importlib.import_module("src.systems.sfp.system")
    return module.SFPSystem


def _make_system(SFPSystem, gen_text):
    """Instantiate without loading a real model; stub generation to ``gen_text``.

    ``gen_text`` may be a string (constant) or a list (one per call, popped).
    """
    SFPSystem._load_model = lambda self: None  # type: ignore
    sysobj = SFPSystem()
    sysobj._tokenizer = object()
    sysobj._model = object()
    sysobj._count_tokens = lambda messages: 0  # type: ignore

    texts = list(gen_text) if isinstance(gen_text, list) else None

    def fake_raw_generate(extra_user_suffix=""):
        if texts is not None:
            return (texts.pop(0), 10, 5)
        return (gen_text, 10, 5)

    sysobj._raw_generate = fake_raw_generate  # type: ignore
    return sysobj


def run_tests() -> None:
    tmp = tempfile.mkdtemp(prefix="clbench_stub_")
    _build_stub_clbench(tmp)
    SFPSystem = _load_system_class(tmp)
    from src.interface import Observation, Query  # noqa: E402

    # 1. JSON extraction variants -------------------------------------------
    assert SFPSystem._extract_json('{"move": "call"}') == {"move": "call"}
    assert SFPSystem._extract_json(
        'Sure! ```json\n{"move": "raise", "amount": 50}\n```'
    ) == {"move": "raise", "amount": 50}
    assert SFPSystem._extract_json(
        'I think {"move": "fold"} is best.'
    ) == {"move": "fold"}
    assert SFPSystem._extract_json("no json here") is None
    # Nested braces stay balanced.
    assert SFPSystem._extract_json('{"a": {"b": 1}}') == {"a": {"b": 1}}
    print("[ok] JSON extraction (plain / fenced / embedded / nested / none)")

    # 2. Clean respond() returns a validated action -------------------------
    s = _make_system(SFPSystem, '{"move": "raise", "amount": 100}')
    q = Query(prompt="Your move?", response_schema=PokerAction)
    resp = s.respond(q)
    assert isinstance(resp.action, PokerAction)
    assert resp.action.move == "raise" and resp.action.amount == 100
    assert len(s.consume_usage_events()) == 1
    print("[ok] respond() returns schema-validated action + records usage")

    # 3. Repair loop: first reply invalid, second valid ---------------------
    s = _make_system(
        SFPSystem,
        ["not json at all", '{"move": "check"}'],
    )
    resp = s.respond(Query(prompt="Move?", response_schema=PokerAction))
    assert resp.action.move == "check"
    print("[ok] repair loop recovers from a malformed first reply")

    # 4. observe() accumulates feedback into context ------------------------
    s = _make_system(SFPSystem, '{"move": "fold"}')
    s.respond(Query(prompt="Hand 1", response_schema=PokerAction))
    s.observe(Observation(content="You lost 20 chips. Opponent bluffs often."))
    assert any("FEEDBACK" in m["content"] for m in s.messages)
    feedback_in_context = sum("FEEDBACK" in m["content"] for m in s.messages)
    assert feedback_in_context == 1
    print("[ok] observe() injects feedback for experiential learning")

    # 5. reset() clears history ---------------------------------------------
    s.reset()
    assert s.messages == [] and s.interaction_count == 0
    print("[ok] reset() clears in-context history")

    # 6. Fallback when the model never emits valid JSON ---------------------
    class Defaultable(BaseModel):
        move: str = "fold"

    s = _make_system(SFPSystem, ["garbage", "still garbage", "nope"])
    s.max_parse_retries = 2
    resp = s.respond(Query(prompt="Move?", response_schema=Defaultable))
    assert resp.action.move == "fold"  # default-constructed fallback
    print("[ok] graceful fallback to schema default after exhausting retries")

    print("\nAll SFP bridge tests passed.")


if __name__ == "__main__":
    run_tests()
