# Limitations

This project is an educational demonstration built for a hackathon timeline. It is not a research artifact and not a reference implementation. The limitations below are grouped by where they originate.

## 1. Model fidelity to BDH

- **This is not the Dragon Hatchling (BDH) architecture.** BDH is a scale-free graph of locally-interacting neuron particles with excitatory/inhibitory circuits, spiking (integrate-and-fire) dynamics, and sparse (~5% active), positive-only activations. None of that is implemented here.
- **The Hebbian update rule is a simplified pedagogical proxy**, not the potentiation rule described in the BDH paper.
- **No thermodynamic capacity bounds.** The paper discusses formal capacity limits on the synaptic memory; this toy model has no such analysis — the matrix simply saturates empirically under the chosen decay/sparsity, without a theoretical bound being derived or enforced.
- **No spiking neurons, no integrate-and-fire cycle, no excitatory/inhibitory split.** The toy update is a single, dense in-place matrix operation, not the graph dynamics BDH is built around.

## 2. Data realism

- **Token activations are synthetic and random** (`random_sparse_pattern`), not real language-model embeddings and not derived from any actual text corpus.
- **There is no language-modeling task.** The comparison is about memory *footprint and growth*, not about prediction quality, perplexity, or any downstream task performance. No claim is made (or can be made) about how this toy model would perform if used to actually process language.

## 3. Comparison methodology

- **The KV-cache figure is an analytical estimate**, computed from `hidden_size` and `n_layers` via the standard byte formula, not measured from a running Transformer. Real-world KV-cache behavior (quantization, multi-query/grouped-query attention, paging, etc.) is not modeled.
- **A single toy configuration is used as "the" comparison.** Only a handful of decay/sparsity values were swept; the results are illustrative trends, not a systematic hyperparameter study, and shouldn't be read as optimized or exhaustive.
- **Saturation is detected heuristically** (recent standard deviation of the norm), not derived from a closed-form stability condition.

## 4. Engineering / demo limitations

- **The precomputed-JSON approach means the artifact is not a live simulator.** A visitor cannot change `n_neurons`, `decay`, `learning_rate`, or `sparsity` and see new results — only the configurations that were explicitly exported ahead of time are viewable.
- **File sizes are large for a static demo.** Storing the full synaptic matrix at every one of 500 steps makes `simulation.json` ~78 MB and `bundle.json` ~44 MB. This is workable for a local hackathon demo but would need frame-subsampling, delta-encoding, or a smaller matrix/step count before being served over a real network.
- **No versioning on the JSON contract.** If `model.py` or `simulation.py` change their output shape, any previously generated `artifact/precomputed/*.json` files become silently incompatible with the frontend — there is no schema check to catch this.
- **Reproducibility is seed-based only.** A single `random_seed=42` is used throughout; no variance-across-seeds analysis was done, so reported numbers (e.g., "final norm 2.443") reflect one run, not a distribution.

## 5. Scope boundary

Everything above should be read alongside `learning_objectives.md`: the project intentionally narrows its claims to "fixed-size vs. growing memory," and every limitation listed here is a consequence of keeping that scope small enough to finish and explain within a hackathon.