# Background Paper

## Source

This project is inspired by, but does not implement, the following paper:

**"The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"**
Pathway (2025). arXiv:2509.26507. Also known as Baby Dragon Hatchling (BDH).

## What the paper proposes

The paper introduces BDH, a large language model architecture built around a scale-free, biologically-inspired network of locally-interacting neuron particles rather than the centralized matrix multiplications used by standard Transformer attention. A few of its central claims, as reported by the authors and by independent coverage of the work:

- Attention-like behavior can emerge from local, graph-based neuron interactions instead of a single global attention matrix.
- The model's working memory during inference relies entirely on synaptic plasticity: Hebbian learning between spiking neurons, rather than a stored buffer of past key/value vectors.
- Activity is sparse (on the order of a few percent of neurons active at a time) and non-negative, closer in spirit to sparse distributed representations than to dense floating-point activations.
- The architecture admits a GPU-friendly "dual" formulation alongside its graph formulation, and the authors report it matches GPT-2-level performance at parameter counts from roughly 10 million to 1 billion on language and translation tasks.
- Individual synapses were observed to strengthen reproducibly when the model processes a specific concept, which the authors present as evidence of interpretable, near-monosemantic internal representations.
- Because working memory lives in synaptic weights rather than an ever-growing cache, the authors position BDH as a candidate for models that generalize and adapt over long stretches of interaction, unlike Transformers, which are static once trained and are bounded by a fixed context window.

## What this project borrows, and what it deliberately leaves out

This project borrows exactly one comparison from the paper's framing: **fixed-size, in-place synaptic memory vs. a memory buffer that grows with sequence length.** That single contrast is implemented as a minimal, from-scratch toy model (see `architecture.md`) so it can be visualized interactively.

Everything else in the paper — the scale-free graph topology, excitatory/inhibitory neuron populations, spiking integrate-and-fire dynamics, the GPU-friendly dual formulation, the empirical language-modeling results at GPT-2 scale, and the monosemanticity findings — is **not** reproduced here. See `limitations.md` for the full list of what the toy model does not attempt.

## Why cite the paper at all

The toy model's entire motivation — "why would fixed-size memory matter?" — only makes sense in reference to the architecture that motivated it. Citing the source keeps the project's claims honest: the interesting scientific claims belong to the original authors, and this project's contribution is a small, explanatory visualization built on top of one idea from their work, not a validation or extension of the architecture itself.

## References

- Pathway, "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain," arXiv:2509.26507, 2025. https://arxiv.org/abs/2509.26507
- Pathway project page / GitHub: bdh (Baby Dragon Hatchling)