# Disclosure

This document states plainly what this project is, what it is not, and what tools were used to build it, so judges, reviewers, and future contributors don't have to infer any of it.

## 1. This is not the Dragon Hatchling (BDH) architecture

Nothing in this repository implements, reproduces, or benchmarks BDH as described in Pathway's paper (arXiv:2509.26507). The Hebbian memory model here is an original, deliberately simplified toy built for pedagogical purposes. Any resemblance to BDH is limited to the single conceptual contrast this project visualizes: fixed-size synaptic memory vs. growing KV-cache memory. See `paper.md` and `limitations.md` for the full boundary between the two.

## 2. Synthetic data disclosure

All token activations used in the simulations are randomly generated (`random_sparse_pattern`, fixed seed `42`) and are not derived from real text, a real language model, or any third-party dataset. No claims in this project are based on real language-modeling performance.

## 3. Estimated, not measured, comparisons

The Transformer KV-cache figures shown throughout (notebooks, artifact, and docs) are computed analytically from a hypothetical model shape (`hidden_size=768`, `n_layers=12`), not measured from a running Transformer. They are estimates of theoretical memory footprint, not benchmark results.

## 4. Use of AI assistance

Portions of this project's documentation (`architecture.md`, `design_decisions.md`, `learning_objectives.md`, `limitations.md`, `paper.md`, `citations.md`, this file, and the license files) were drafted with the assistance of Claude (Anthropic), based on the contents of the project's own notebooks and source code, plus a web search used to verify factual claims about the BDH paper. All technical content was derived from the actual notebook outputs and code in this repository; where background research was used (the BDH paper summary in `paper.md`), sources are listed in `citations.md`.

If your hackathon's rules require a specific format or level of detail for AI-assistance disclosure, please adapt this section accordingly — the statement above is a factual account, not a rules-compliant template for any particular competition.

## 5. No warranty of scientific validity

This project makes no claim to be a validated scientific result. It is an educational artifact built to build intuition about one architectural trade-off. See `limitations.md` for the complete list of simplifications.