# SFP × CL-Bench integration

A bridge that evaluates **SFP-trained checkpoints** on
[CL-Bench](https://github.com/pgasawa/continual-learning-bench)
(`pgasawa/continual-learning-bench`), an in-context experiential-learning
benchmark.

## Why — and what this is *not*

These two projects measure different things, and it's important not to conflate
them:

| | SFP (this repo) | CL-Bench |
|---|---|---|
| Level | **Weight-space** | **In-context** |
| Mechanism | Regularizes activation drift during *fine-tuning* so old tasks survive | Agent accumulates feedback across episodes and improves **with no weight update** |
| Metric | retention × plasticity (harmonic mean) | `mean_gain` = stateful reward − stateless baseline reward |

So **"train with SFP → run CL-Bench → gain goes up" is not a mechanical
guarantee.** SFP does not participate in the in-context loop; it only shapes the
frozen weights the loop runs on.

What this bridge *does* let you test is a genuine, open question that SFP's own
benchmark cannot answer:

> **Is a model that was protected from catastrophic forgetting a better *base*
> for in-context experiential learning than a naively fine-tuned one?**

i.e. does preserving capabilities in weight space also preserve (or improve) the
model's ability to learn from experience in context? The bridge runs both arms —
naive base vs. SFP-protected checkpoint — through the identical CL-Bench loop so
their `mean_gain` is directly comparable.

## Components

| File | Role |
|---|---|
| `sfp_system/` | A CL-Bench `system` (`@register_system("sfp")`) that loads a local HF / SFP checkpoint with `transformers`+`peft` and runs it through CL-Bench's experiential loop. One class serves **both** experiment arms. |
| `install_adapter.py` | Copies/symlinks `sfp_system/` into a CL-Bench checkout at `src/systems/sfp/`. |
| `test_sfp_system.py` | Offline tests (no GPU / no download) for JSON extraction, schema-validation/repair, `observe`/`reset`, fallback. |
| `../export.py` | Merges an SFP LoRA adapter into a standalone HF model (for `--system.merged_path`, or for serving via vLLM/TGI). |

## End-to-end workflow

### 1. Train the two arms with SFP (in *this* repo)

```bash
# treatment: SFP-protected sequential fine-tune
python train.py --config configs/full.yaml --method sfp --out_dir out/sfp_run

# control: same schedule, no mitigation
python train.py --config configs/full.yaml --method naive --out_dir out/naive_run
```

Each run writes LoRA adapters to `out/<run>/task_<N>/` (N = last task index).

### 2. (Optional) merge an adapter into a standalone model

```bash
python export.py --base Qwen/Qwen2.5-1.5B-Instruct \
    --adapter out/sfp_run/task_4 --out out/sfp_run/merged
```

### 3. Install the bridge into CL-Bench

```bash
git clone https://github.com/pgasawa/continual-learning-bench.git
python clbench/install_adapter.py --clbench ./continual-learning-bench
cd continual-learning-bench
uv sync --all-extras
uv pip install torch transformers peft accelerate   # local-model backends
uv run clbench list                                  # 'sfp' should appear
```

### 4. Run both arms and compare `mean_gain`

```bash
# control — bare base model
clbench run exploitable_poker --system sfp --schedule quick_test \
    --system.model Qwen/Qwen2.5-1.5B-Instruct

# treatment — SFP-protected checkpoint (adapter or merged)
clbench run exploitable_poker --system sfp --schedule quick_test \
    --system.model Qwen/Qwen2.5-1.5B-Instruct \
    --system.adapter_path /abs/path/to/out/sfp_run/task_4
```

The treatment arm wins the hypothesis only if its `mean_gain` is meaningfully
higher than the control's, across seeds/tasks.

## `--system.*` knobs

Passed on the `clbench run` command line (introspected from `SFPSystem.__init__`):

| Param | Default | Meaning |
|---|---|---|
| `model` | `Qwen/Qwen2.5-1.5B-Instruct` | Base HF model id/path |
| `adapter_path` | `""` | LoRA adapter dir from an SFP run; empty = base only (control) |
| `merged_path` | `""` | Pre-merged HF dir (from `export.py`); overrides `model`/`adapter_path` |
| `max_context_tokens` | `8192` | Context window before FIFO truncation |
| `max_new_tokens` | `512` | Generation budget per turn |
| `temperature` | `0.0` | `0.0` = greedy/deterministic |
| `device` | `auto` | `auto`/`cuda`/`cpu`/`mps` |
| `max_parse_retries` | `2` | Extra attempts to coax schema-valid JSON |

## Recommended model & config

Within the range SFP has actually been validated on (H1 holds at 1.5B, fails at
135M), the practical pick is **Qwen2.5-1.5B-Instruct** — it follows JSON-schema
instructions well enough for CL-Bench's structured actions, and matches
`configs/full.yaml` (`sfp_lambda: 0.1`, `lora_rank: 64`, `memory: 128`).

**Caveat on signal strength.** CL-Bench's agentic tasks (e.g. `exploitable_poker`)
were designed around frontier-scale models, where reported in-context gain is
~20%. At 1.5B, absolute gain may be small and noisy for *both* arms — the
interesting quantity is the **difference** between SFP and naive, not the
absolute number. Treat 1.5B as the validated lower bound; 7B+ would give a
stronger signal but is outside SFP's tested range in this repo.

## Tests

```bash
python clbench/test_sfp_system.py   # offline; needs only pydantic
```
