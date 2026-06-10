"""
export.py — Merge a trained SFP LoRA adapter into a standalone HuggingFace model.

``train.py`` saves only LoRA adapter weights under ``out/<run>/task_<N>/`` to
keep checkpoints small. Some downstream consumers — an OpenAI-compatible serving
backend (vLLM/TGI), or the CL-Bench bridge system's ``merged_path`` option —
want a plain, self-contained HF model directory instead of base + adapter.

This script loads the base model, attaches the adapter, fuses the LoRA deltas
into the base weights (``merge_and_unload``), and writes the result plus the
tokenizer to ``--out``.

Usage:
    python export.py \\
        --base Qwen/Qwen2.5-1.5B-Instruct \\
        --adapter out/sfp_run/task_4 \\
        --out out/sfp_run/merged

Then point the CL-Bench system at it:
    clbench run exploitable_poker --system sfp --system.merged_path out/sfp_run/merged
"""

from __future__ import annotations

import argparse
import os


def merge_adapter(base: str, adapter: str, out: str, device: str = "cpu") -> str:
    """Merge ``adapter`` into ``base`` and save the standalone model to ``out``.

    Args:
        base: Base HF model id or path the adapter was trained on.
        adapter: Path to the LoRA adapter directory (e.g. ``out/run/task_4``).
        out: Destination directory for the merged model + tokenizer.
        device: Device to load on while merging ("cpu" is fine and memory-safe).

    Returns:
        The output directory path.
    """
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not os.path.isdir(adapter):
        raise FileNotFoundError(f"Adapter directory not found: {adapter}")

    dtype = torch.bfloat16 if device != "cpu" else torch.float32

    print(f"Loading base model: {base}")
    model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=dtype)
    model = model.to(device)

    print(f"Attaching adapter: {adapter}")
    model = PeftModel.from_pretrained(model, adapter)

    print("Merging LoRA weights into base...")
    model = model.merge_and_unload()

    os.makedirs(out, exist_ok=True)
    print(f"Saving merged model to: {out}")
    model.save_pretrained(out)

    tokenizer = AutoTokenizer.from_pretrained(base)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.save_pretrained(out)

    print("Done.")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        required=True,
        help="Base HF model id/path the adapter was trained on.",
    )
    parser.add_argument(
        "--adapter",
        required=True,
        help="Path to the LoRA adapter dir, e.g. out/sfp_run/task_4.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for the merged standalone model.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help='Device for the merge ("cpu", "cuda"). Default: cpu.',
    )
    args = parser.parse_args()
    merge_adapter(args.base, args.adapter, args.out, device=args.device)


if __name__ == "__main__":
    main()
