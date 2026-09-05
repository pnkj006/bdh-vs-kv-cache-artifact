# Architecture

## Overview

The project is split into three layers that never overlap in responsibility:

1. **A Python backend** (`src/`) that owns every piece of scientific computation.
2. **Two notebooks** (`notebooks/`) that drive the backend — one for exploration, one for export.
3. **A static frontend artifact** (`artifact/`) that only reads pre-generated JSON and renders it.

This separation is the core architectural decision of the project: the browser never computes anything scientific, it only visualizes numbers that were computed and validated ahead of time in Python.

```
src/
    model.py        # Hebbian memory primitives
    simulation.py    # sequence simulation + precomputed bundle builders
    evaluation.py    # aggregate diagnostics (norm growth, saturation, decay/sparsity sweeps)
    utils.py         # I/O helpers (save_json, ensure_directory)

notebooks/
    toy_model.ipynb           # exploratory analysis, plots, sweeps, evaluation
    generate_precomputed.ipynb # deterministic export of artifact/precomputed/*.json

artifact/
    precomputed/
        memory_curve.json
        simulation.json
        metrics.json
        bundle.json
    (frontend code that fetches the files above)
```

## Component responsibilities

### `model.py`
Defines the fixed-size Hebbian memory primitive:
- `HebbianConfig` — the tunable parameters of the toy model (`n_neurons`, `decay`, `learning_rate`, `sparsity`).
- `HebbianMemory` — holds the synaptic weight matrix `W` (shape `n_neurons × n_neurons`) and applies Hebbian-style updates in place.
- `random_sparse_pattern` — generates synthetic sparse activation vectors used as stand-ins for token embeddings.
- `compare_memory` — computes the fixed Hebbian footprint against an equivalent Transformer KV-cache footprint for a given sequence length.

### `simulation.py`
Runs the model over a synthetic token stream and packages results:
- `SimulationConfig` — sequence length, random seed, and the reference Transformer shape (`hidden_size`, `n_layers`) used only to estimate KV-cache size.
- `simulate_sequence` — steps through `n_tokens` tokens, updating the synaptic matrix and recording a frame (`step`, `matrix`, `norm`) per token.
- `generate_memory_curve` — produces the KV-cache-vs-Hebbian-memory comparison curve across a range of sequence lengths.
- `generate_metrics` — summary statistics for a single run (final norm, weight extremes, active synapse count).
- `build_precomputed_bundle` — assembles the single `bundle.json` consumed by the artifact in one shot.

### `evaluation.py`
Higher-level diagnostics used only inside `toy_model.ipynb` for exploratory analysis, not exported to the artifact:
- `full_evaluation` — returns norm growth, saturation detection, weight statistics, the memory-scaling comparison, and decay/sparsity sweeps.

### `utils.py`
Thin I/O helpers (`save_json`, `ensure_directory`) shared by both notebooks so the JSON-writing logic isn't duplicated.

## Data flow

```
HebbianConfig + SimulationConfig
        │
        ▼
 toy_model.ipynb  ──(exploration, plots, sweeps)──▶  intuition / write-up
        │
        │  (same config values, copied into)
        ▼
 generate_precomputed.ipynb
        │
        ▼
 artifact/precomputed/*.json  ◀── the contract between backend and frontend
        │
        ▼
 frontend fetch("precomputed/...")  ──▶  interactive visualization
```

`toy_model.ipynb` is where the science happens and is validated (norm growth curves, decay sweeps, sparsity sweeps, saturation checks). `generate_precomputed.ipynb` re-runs the same model with the finalized configuration and writes exactly four JSON files that the frontend depends on. No notebook logic is imported by the frontend; the JSON files are the only interface between the two sides.

## The precomputed contract

| File | Shape | Purpose |
|---|---|---|
| `memory_curve.json` | `{tokens, kv_memory, hebbian_memory}` | Sequence length vs. memory footprint (GiB) for KV-cache vs. Hebbian memory — the headline comparison. |
| `simulation.json` | `{frames: [{step, matrix, norm}], norms}` | Token-by-token evolution of the synaptic matrix, used to animate/scrub through the simulation. |
| `metrics.json` | flat dict of scalars | Final-state summary stats for the run (final norm, min/max/mean weight, active synapse count). |
| `bundle.json` | combined payload | Single-fetch convenience bundle for the artifact. |

Because `simulation.json` stores the full weight matrix at every one of the 500 steps, it is by far the largest file (tens of MB) — see `limitations.md` for the consequences of that choice.

## Why this shape

- **Backend/frontend split** guarantees the demo is reproducible and that no visitor's browser has to run NumPy-equivalent math.
- **Two notebooks instead of one** keeps exploratory, throwaway analysis (plots, print statements, sweeps) separate from the deterministic export step that the artifact actually depends on.
- **A fixed JSON contract** means the frontend can be developed and iterated on independently of the Python code, as long as the four file names and their keys stay stable.