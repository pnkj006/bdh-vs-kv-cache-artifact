# Learning Objectives

This project exists to build intuition for one specific idea from the Dragon Hatchling (BDH) paper: that a biologically-inspired architecture can replace a Transformer's growing KV-cache with a **fixed-size synaptic memory** updated via Hebbian learning. Everything below is scoped to what the toy model and interactive artifact can actually demonstrate — not to teaching the full BDH architecture.

## By the end of this project, a learner should be able to:

1. **Explain the core memory trade-off.**
   State, in plain terms, why Transformer KV-cache memory grows linearly with sequence length while a Hebbian synaptic matrix stays a fixed size regardless of how many tokens are processed.

2. **Build and reason about a minimal Hebbian memory.**
   Understand the mechanics of a fixed-size synaptic matrix that is updated in place, token by token, rather than appended to.

3. **Read a norm-growth curve.**
   Interpret the Frobenius norm of the synaptic matrix over a token sequence, and understand why it typically grows and then stabilizes rather than growing forever.

4. **Connect two model hyperparameters to observable behavior.**
   - *Decay*: see how increasing decay suppresses runaway norm growth (empirically: final norm ~32 at decay=0 vs. ~2.4 at decay=0.10 over 500 tokens).
   - *Sparsity*: see how activation sparsity controls the density of the synaptic matrix, and that this relationship saturates rather than scaling linearly.

5. **Quantify the memory-scaling gap.**
   Compare actual numbers — e.g., a fixed 16 KiB Hebbian footprint against a KV-cache that grows from single-digit MiB to over a GiB as sequence length increases from hundreds to tens of thousands of tokens — and understand what "fixed-size" buys you as context grows.

6. **Distinguish a pedagogical proxy from the real architecture.**
   Correctly state that this toy model is *not* BDH: it omits spiking dynamics, excitatory/inhibitory circuits, integrate-and-fire cycles, and the thermodynamic capacity bounds described in the original paper, and know where to go (the original paper) for anything beyond the toy comparison.

7. **Use the interactive artifact as an exploration tool, not a black box.**
   Know that every number the artifact shows was precomputed by a specific, inspectable Python function (`generate_memory_curve`, `simulate_sequence`, `generate_metrics`), and be able to trace any displayed value back to the notebook that produced it.

## Non-goals

To keep the scope honest, this project deliberately does **not** aim to teach:
- The full BDH graph/neuron-particle formalism or its GPU-friendly dual formulation.
- Spiking neuron dynamics or integrate-and-fire thresholding.
- Any actual language-modeling task or benchmark comparable to GPT-2-scale results.
- General Transformer internals beyond the KV-cache memory formula used for comparison.