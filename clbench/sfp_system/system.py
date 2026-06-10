"""
SFP bridge system for the Continual Learning Benchmark (CL-Bench).

This adapter lets a HuggingFace checkpoint produced by this repository's
``train.py`` be evaluated *as a CL-Bench system*. It exists to answer a
question SFP's own benchmark does not: **is a model that was protected against
catastrophic forgetting during fine-tuning a better base for in-context
experiential learning?**

Two paradigms meet here:

* **SFP** (this repo) regularizes *weight-space* drift during sequential
  fine-tuning so old capabilities survive new training.
* **CL-Bench** measures *in-context* online improvement ("gain") — the model
  accumulates feedback across episodes and gets better **without** any weight
  update.

The bridge does not make SFP "boost gain" mechanically. It loads a frozen SFP
(or naive) checkpoint and runs it through CL-Bench's experiential loop so the
two arms can be compared on equal footing.

Drop this package into a CL-Bench checkout at ``src/systems/sfp/`` (see
``clbench/install_adapter.py``). Then, from the CL-Bench repo::

    # naive base model (control arm)
    clbench run exploitable_poker --system sfp --schedule quick_test \\
        --system.model Qwen/Qwen2.5-1.5B-Instruct

    # SFP-protected checkpoint (treatment arm)
    clbench run exploitable_poker --system sfp --schedule quick_test \\
        --system.model Qwen/Qwen2.5-1.5B-Instruct \\
        --system.adapter_path /abs/path/to/out/sfp_run/task_4

Compare the ``mean_gain`` reported for each.

Relative imports (``from ...interface``) resolve only when this file lives at
``<clbench>/src/systems/sfp/system.py`` — mirroring the bundled ``icl`` system.
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from pydantic import BaseModel, ValidationError

from ...interface import (
    ContinualLearningSystem,
    Observation,
    Query,
    Response,
)
from ...registry import register_system
from ...usage import UsageEvent


@register_system("sfp")
class SFPSystem(ContinualLearningSystem):
    """In-context system backed by a local HuggingFace / SFP checkpoint.

    Accumulates the full interaction history (queries + task feedback) in a
    chat-style context with FIFO token truncation, exactly like the ``icl``
    baseline — the only difference is the model runs locally in-process via
    ``transformers`` instead of through a hosted API, so a checkpoint trained
    by this repo's ``train.py`` can be evaluated directly.

    The same class serves both experiment arms:

    * No ``adapter_path`` / ``merged_path`` -> the bare base model (naive
      control).
    * ``adapter_path`` -> base model + LoRA adapter from an SFP run
      (``out/<run>/task_<N>``).
    * ``merged_path`` -> a standalone merged HF folder (see ``export.py``).
    """

    # A single in-process GPU model must not be cloned across parallel workers.
    parallel_safe = False

    def __init__(
        self,
        model: str = "Qwen/Qwen2.5-1.5B-Instruct",
        adapter_path: str = "",
        merged_path: str = "",
        max_context_tokens: int = 8192,
        max_new_tokens: int = 512,
        temperature: float = 0.0,
        reserve_tokens: int = 768,
        device: str = "auto",
        system_prompt: str = "",
        max_parse_retries: int = 2,
        name: str = "sfp",
    ):
        """Initialize the SFP-backed system.

        Args:
            model: Base HF model id or local path. Ignored when ``merged_path``
                is set.
            adapter_path: Path to a LoRA adapter directory from an SFP run
                (e.g. ``out/sfp_run/task_4``). Empty -> base model only.
            merged_path: Path to a pre-merged standalone HF model directory
                (produced by ``export.py``). Takes precedence over
                ``model``/``adapter_path``.
            max_context_tokens: Context window before FIFO truncation kicks in.
            max_new_tokens: Generation budget per turn.
            temperature: Sampling temperature. ``0.0`` -> greedy/deterministic.
            reserve_tokens: Headroom kept free for the response + chat scaffolding.
            device: ``"auto"``, ``"cuda"``, ``"cpu"``, or ``"mps"``.
            system_prompt: Optional system prompt prepended to every call.
            max_parse_retries: Extra attempts to coax valid schema-conforming
                JSON out of the model before giving up on a turn.
            name: System identifier surfaced in CL-Bench manifests/traces.
        """
        self._name = name
        self.model_id = model
        self.adapter_path = adapter_path.strip()
        self.merged_path = merged_path.strip()
        self.max_context_tokens = max_context_tokens
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.reserve_tokens = reserve_tokens
        self.device = device
        self.system_prompt = system_prompt
        self.max_parse_retries = max_parse_retries

        # Conversation history shared across episodes — this is what lets the
        # model learn from experience in-context.
        self.messages: list[dict[str, str]] = []
        self.interaction_count = 0

        self._model = None
        self._tokenizer = None
        self._resolved_device: str = device
        self._load_model()

    # ------------------------------------------------------------------ #
    # Model loading
    # ------------------------------------------------------------------ #
    def _load_model(self) -> None:
        """Load the tokenizer + (optionally adapted) causal LM into memory."""
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        device = self.device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self._resolved_device = device

        dtype = torch.bfloat16 if device != "cpu" else torch.float32

        source = self.merged_path or self.model_id
        tokenizer = AutoTokenizer.from_pretrained(source)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model_kwargs: dict[str, Any] = {"torch_dtype": dtype}
        if device == "cuda":
            model_kwargs["device_map"] = "auto"

        model = AutoModelForCausalLM.from_pretrained(source, **model_kwargs)

        # Attach a LoRA adapter from an SFP run if one was requested and we are
        # not already loading a pre-merged folder.
        if self.adapter_path and not self.merged_path:
            from peft import PeftModel

            model = PeftModel.from_pretrained(model, self.adapter_path)

        if "device_map" not in model_kwargs:
            model = model.to(device)
        model.eval()

        if model.config.pad_token_id is None:
            model.config.pad_token_id = tokenizer.pad_token_id

        self._model = model
        self._tokenizer = tokenizer

    # ------------------------------------------------------------------ #
    # ContinualLearningSystem interface
    # ------------------------------------------------------------------ #
    def respond(self, query: Query) -> Response:
        """Produce a schema-conforming action for the current task turn."""
        self.interaction_count += 1

        prompt = query.prompt or "(no content)"
        schema_block = self._schema_instructions(query.response_schema)
        self._add_message("user", f"{prompt}\n\n{schema_block}")
        self._truncate_context()

        action, raw_text, in_tok, out_tok = self._generate_action(
            query.response_schema
        )

        # Record what the model actually emitted so it stays in context for
        # subsequent turns (experiential continuity).
        self._add_message("assistant", raw_text)

        self.record_usage_event(
            UsageEvent(
                call_type="local_generate",
                model=self._artifact_label(),
                provider="local",
                input_tokens=in_tok,
                output_tokens=out_tok,
                total_tokens=(in_tok or 0) + (out_tok or 0),
                cost_usd=0.0,
                pricing_source="local",
            )
        )

        return Response(
            action=action,
            metadata={
                "interaction_count": self.interaction_count,
                "system_type": "sfp",
                "model": self.model_id,
                "adapter_path": self.adapter_path or None,
                "merged_path": self.merged_path or None,
                "context_messages": len(self.messages),
            },
        )

    def observe(
        self, observation: Observation, next_query: Optional[Query] = None
    ) -> None:
        """Persist task feedback into context — the experiential signal."""
        content = (observation.content or "").strip()
        if not content:
            return
        self._add_message("user", f"FEEDBACK: {content}")
        self._truncate_context()

    def reset(self) -> None:
        """Clear conversation history for a fresh task instance."""
        self.messages = []
        self.interaction_count = 0

    @property
    def name(self) -> str:
        return self._name

    def get_run_artifacts(self) -> dict[str, Any]:
        """Expose the final in-context state for offline analysis."""
        return {
            "artifact_type": "sfp",
            "model": self.model_id,
            "adapter_path": self.adapter_path or None,
            "merged_path": self.merged_path or None,
            "message_count": len(self.messages),
            "interaction_count": self.interaction_count,
            "messages": list(self.messages),
        }

    # ------------------------------------------------------------------ #
    # Generation + structured-output parsing
    # ------------------------------------------------------------------ #
    def _generate_action(
        self, schema: type[BaseModel]
    ) -> tuple[BaseModel, str, int, int]:
        """Generate and validate an action, repairing malformed JSON on retry.

        Returns ``(action, raw_assistant_text, input_tokens, output_tokens)``.
        Falls back to a schema default (when constructible) rather than crashing
        the whole run on a single bad turn.
        """
        repair_suffix = ""
        last_text = ""
        total_in = 0
        total_out = 0

        for attempt in range(self.max_parse_retries + 1):
            text, in_tok, out_tok = self._raw_generate(repair_suffix)
            total_in += in_tok
            total_out += out_tok
            last_text = text

            candidate = self._extract_json(text)
            if candidate is not None:
                try:
                    action = schema.model_validate(candidate)
                    return action, text, total_in, total_out
                except ValidationError as err:
                    repair_suffix = (
                        "\n\nYour previous reply did not satisfy the schema:\n"
                        f"{err}\n"
                        "Reply again with ONLY a valid JSON object."
                    )
            else:
                repair_suffix = (
                    "\n\nYour previous reply contained no parseable JSON object. "
                    "Reply with ONLY a single JSON object matching the schema."
                )

        # Last resort: try a zero-arg / default-constructed instance so the
        # benchmark can keep moving and the failure shows up as a bad action
        # rather than a hard crash.
        try:
            fallback = schema()  # type: ignore[call-arg]
        except (ValidationError, TypeError):
            raise RuntimeError(
                "SFP system could not produce schema-valid JSON after "
                f"{self.max_parse_retries + 1} attempts. Last output:\n{last_text}"
            )
        return fallback, last_text, total_in, total_out

    def _raw_generate(self, extra_user_suffix: str) -> tuple[str, int, int]:
        """Run one decode pass over the current context. Returns text + tokens."""
        import torch

        messages = self._chat_messages()
        if extra_user_suffix:
            messages = [
                *messages,
                {"role": "user", "content": extra_user_suffix.strip()},
            ]

        inputs = self._tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to(self._model.device)

        input_len = inputs.shape[1]
        gen_kwargs: dict[str, Any] = {
            "max_new_tokens": self.max_new_tokens,
            "pad_token_id": self._tokenizer.pad_token_id,
        }
        if self.temperature and self.temperature > 0:
            gen_kwargs.update(do_sample=True, temperature=self.temperature)
        else:
            gen_kwargs.update(do_sample=False)

        with torch.no_grad():
            out = self._model.generate(inputs, **gen_kwargs)

        new_tokens = out[0][input_len:]
        text = self._tokenizer.decode(new_tokens, skip_special_tokens=True)
        return text.strip(), int(input_len), int(new_tokens.shape[0])

    @staticmethod
    def _extract_json(text: str) -> Optional[dict]:
        """Best-effort extraction of the first balanced JSON object in ``text``."""
        if not text:
            return None

        # Strip ```json fences if present.
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass

        start = text.find("{")
        while start != -1:
            depth = 0
            in_str = False
            esc = False
            for i in range(start, len(text)):
                ch = text[i]
                if in_str:
                    if esc:
                        esc = False
                    elif ch == "\\":
                        esc = True
                    elif ch == '"':
                        in_str = False
                    continue
                if ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        blob = text[start : i + 1]
                        try:
                            return json.loads(blob)
                        except json.JSONDecodeError:
                            break  # try next '{'
            start = text.find("{", start + 1)
        return None

    @staticmethod
    def _schema_instructions(schema: type[BaseModel]) -> str:
        """Render the response schema as an explicit instruction block."""
        try:
            schema_json = json.dumps(schema.model_json_schema(), indent=2)
        except Exception:  # pragma: no cover - defensive
            schema_json = "{}"
        return (
            "Respond with ONLY a single JSON object that conforms to this JSON "
            "schema. Do not include any prose, explanation, or markdown fences.\n"
            f"JSON schema:\n{schema_json}"
        )

    # ------------------------------------------------------------------ #
    # Context bookkeeping
    # ------------------------------------------------------------------ #
    def _chat_messages(self) -> list[dict[str, str]]:
        if self.system_prompt:
            return [{"role": "system", "content": self.system_prompt}, *self.messages]
        return list(self.messages)

    def _add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def _count_tokens(self, messages: list[dict[str, str]]) -> int:
        if not messages:
            return 0
        try:
            ids = self._tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, return_tensors="pt"
            )
            return int(ids.shape[1])
        except Exception:
            # Fall back to a rough char/4 heuristic if templating fails.
            return sum(len(m["content"]) for m in messages) // 4

    def _truncate_context(self) -> None:
        """Drop oldest turns (FIFO) until the context fits the budget."""
        budget = self.max_context_tokens - self.reserve_tokens
        while len(self.messages) > 1:
            if self._count_tokens(self._chat_messages()) <= budget:
                break
            self.messages.pop(0)

    def _artifact_label(self) -> str:
        if self.merged_path:
            return self.merged_path
        if self.adapter_path:
            return f"{self.model_id}+{self.adapter_path}"
        return self.model_id
