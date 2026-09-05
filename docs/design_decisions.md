# Design Decisions

This document records the deliberate choices made while building the project and the reasoning behind each one, so a reviewer doesn't have to reverse-engineer intent from the code.

## 1. Build a toy proxy, not a BDH re-implementation

The Dragon Hatchling (BDH) architecture (Pathway, arXiv 2509.26507) replaces Transformer attention with a scale-free graph of neuron particles that update synapses through Hebbian learning during inference, with sparse (~5% active), excitatory/inhibitory, spiking dynamics. Reimplementing that faithfully was out of scope for a hackathon timeline.

**Decision:** build the smallest possible model that preserves the *one idea* worth communicating — fixed-size synaptic memory vs. growing KV-cache memory — and be explicit everywhere (notebook headers, this document) that it is a pedagogical proxy, not BDH itself. This is why every notebook opens with a disclaimer pointing back to the original paper for anything BDH-specific.

## 2. Precompute everything; the frontend only reads JSON

**Alternative considered:** run the simulation live in the browser (e.g., via Pyodide or a JS reimplementation of the Hebbian update).

**Decision:** compute once in Python, export static JSON, and let the artifact `fetch()` it. This was chosen because:
- It guarantees the numbers shown in the demo match the numbers validated in `toy_model.ipynb` exactly — no risk of a JS reimplementation drifting from the Python one.
- It keeps the frontend dependency-free (no NumPy-in-the-browser, no WASM runtime to debug under hackathon time pressure).
- It cleanly separates "science" from "presentation," which made it possible to iterate on the visualization without touching the model at all.

**Trade-off accepted:** the artifact can only show configurations that were precomputed; it is not a live, user-tunable simulator. See `limitations.md`.

## 3. Two notebooks instead of one

**Decision:** split exploration (`toy_model.ipynb`) from export (`generate_precomputed.ipynb`).

`toy_model.ipynb` is allowed to be messy — plots, print debugging, parameter sweeps over decay and sparsity, a full diagnostic dump via `full_evaluation()`. `generate_precomputed.ipynb` does none of that; it imports the finalized config, calls exactly four generator functions, and writes exactly four files. Keeping the export path this narrow makes it obvious what the frontend's real dependencies are and makes the export reproducible on demand.

## 4. Hebbian configuration values

| Parameter | Value | Reasoning |
|---|---|---|
| `n_neurons` | 64 | Small enough that the synaptic matrix (64×64) is cheap to store per frame and visually legible; large enough to show non-trivial structure. |
| `decay` | 0.05 | The decay sweep (0.00 → 0.15) showed decay=0 lets the norm grow unbounded (~32 at 500 tokens) while higher decay stabilizes it; 0.05 was chosen as a middle ground that still shows growth-then-stabilization rather than either extreme. |
| `learning_rate` | 0.10 | Kept fixed across all experiments so decay and sparsity sweeps isolate a single variable at a time. |
| `sparsity` | 0.10 | The sparsity sweep showed density saturates quickly (near 1.0 by sparsity≈0.2 at this scale); 0.10 sits in the more informative, non-saturated region of that curve. |

## 5. Frobenius norm as the headline memory-magnitude metric

Rather than trying to interpret individual synaptic weights, the norm of the whole matrix is tracked over time. It's a single number that is easy to plot, easy to explain, and directly demonstrates the "grows then stabilizes/saturates" behavior that motivates the decay parameter.

## 6. KV-cache size as an estimate, not a live Transformer

The KV-cache comparison in `memory_curve.json` is computed analytically from `hidden_size` and `n_layers` (i.e., the standard KV-cache byte formula), rather than by running an actual Transformer forward pass. This keeps the comparison fast to generate and deterministic, at the cost of not capturing implementation details of any specific real model (see `limitations.md`).

## 7. Single JSON bundle in addition to individual files

`bundle.json` duplicates the content of the other three files into one payload. This was added purely for frontend convenience (one `fetch()` instead of three) and is the largest file on disk as a direct consequence — a trade-off between network-round-trip simplicity and payload size.