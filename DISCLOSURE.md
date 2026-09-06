# Disclosure

This document explains the scope of this project, the assumptions made during development, and the tools used to create it. Its purpose is to make the educational intent of the repository clear for reviewers, contributors, and users.

---

## 1. Educational Demonstration

This repository is an educational visualization of one architectural idea discussed in the paper:

> **The Dragon Hatchling: Linear-Time Transformer Without Attention**  
> Kosowski et al., 2025  
> https://arxiv.org/abs/2509.26507

The project illustrates the conceptual difference between:

- Transformer KV-cache memory, which grows with sequence length.
- A bounded Hebbian-style synaptic memory that maintains a fixed-size state.

The implementation is intentionally simplified for visualization and learning purposes.

---

## 2. Not an Implementation of BDH

This repository **does not implement, reproduce, benchmark, or validate** the Dragon Hatchling (BDH) architecture.

Instead, it contains an original toy Hebbian memory model inspired only by the high-level idea of maintaining a bounded memory state.

None of the algorithms, training procedures, reasoning equations, or performance claims from the paper are reproduced here.

---

## 3. Synthetic Simulation Data

All simulations use synthetic randomly generated sparse activation patterns.

Specifically,

- activations are generated using `random_sparse_pattern()`
- simulations use a fixed random seed for reproducibility
- no real text, language model outputs, datasets, or embeddings are used

The visualization is therefore intended only to illustrate qualitative behavior.

---

## 4. Analytical Memory Estimates

The Transformer KV-cache memory shown throughout the project is computed analytically from the standard KV-cache memory equation.

The default visualization assumes:

- hidden size = 768
- number of layers = 12
- FP16 (2-byte) precision

These values are configurable and represent theoretical memory requirements rather than measurements from an actual Transformer implementation.

---

## 5. AI-Assisted Development

AI tools were used during the development of this project to assist with:

- documentation drafting
- code review
- frontend development
- JavaScript refactoring
- UI design suggestions
- writing explanations
- improving repository organization

All architecture decisions, implementation choices, educational content, and final verification were performed by the project author.

---

## 6. Scientific Scope

This repository should not be interpreted as scientific evidence supporting or evaluating BDH.

It does **not** provide:

- language-model benchmarks
- accuracy measurements
- training results
- inference speed comparisons
- empirical validation of BDH

Its purpose is solely to help readers build intuition about the memory trade-off between an unbounded KV-cache and a bounded synaptic memory representation.

---

## 7. Citation

This project cites the BDH paper for background and conceptual motivation only.

No figures, code, datasets, or copyrighted material from the paper are redistributed in this repository.

Please cite and consult the original paper for the formal algorithms and theoretical results.

https://arxiv.org/abs/2509.26507