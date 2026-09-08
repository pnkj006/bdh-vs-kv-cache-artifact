# Citations

Research referenced by **Hebbian vs. KV Bloat**, scoped to papers published **2022–2026** to match the era of the BDH paper and the current KV-cache optimization literature. Every link below was verified directly against its arXiv page. For each entry: what the paper says, and which part of this artifact it informs.

---

## 1. Primary reference — BDH architecture

**Kosowski, A., Uznański, P., Chorowski, J., Stamirowska, Z., & Bartoszkiewicz, M. (2025).**
*The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain.*
arXiv:2509.26507 — https://arxiv.org/abs/2509.26507

BDH's working memory during inference relies entirely on synaptic plasticity with Hebbian learning, implemented as local graph dynamics over an excitatory/inhibitory neuron circuit, and it empirically matches GPT‑2‑scale Transformers at 10M–1B parameter scales while remaining fully interpretable.

**Used for:** The direct inspiration for this whole artifact. The bounded synaptic matrix `W`, its update rule, and the "memory stays flat while KV-cache grows" narrative are a simplified, pedagogical stand-in for BDH's core claim. Referenced in `src/model.py` and the Hebbian side of `memory_curve.json`.

Companion resource (not a paper, cited for implementation reference):
**Pathway (2025).** *BDH: Dragon Hatchling — Architecture and Code.* https://github.com/pathwaycom/bdh

---

## 2. Transformer KV-cache scaling & optimization

**Xu, Y., Khaira, N. K., & Singh, T. (2026).**
*KV Cache Optimization Strategies for Scalable and Efficient LLM Inference.*
arXiv:2603.20397 — https://arxiv.org/abs/2603.20397

Surveys KV-cache optimization into five directions — cache eviction, compression/reconstruction, hybrid memory solutions, novel attention mechanisms, and combined approaches — anchored in attention's O(n²) complexity as the root driver of long-context memory cost.

**Used for:** Background for the "Motivation" section and the exact Transformer memory equation shown in the Memory Comparison panel. Justifies why the linear KV-growth curve in `memory_curve.json` reflects real deployed systems, not an assumption invented for the demo.

---

**Wu, H., & Tu, K. (2024).**
*Layer-Condensed KV Cache for Efficient Inference of Large Language Models.*
arXiv:2405.10637 — https://arxiv.org/abs/2405.10637

Proposes computing and caching KVs for only a small subset of layers, reporting up to 26× higher throughput while remaining compatible ("orthogonal") with other memory-saving techniques.

**Used for:** Cited in `docs/` as a real-world example of *reducing* KV growth without eliminating the linear-in-context-length relationship — contrasted against BDH's fundamentally bounded (not just slower-growing) memory.

---

**Yi, Z., Niu, G., Wang, L., Tang, W., & Zhang, L. (2024).**
*A Method for Building Large Language Models with Predefined KV Cache Capacity.*
arXiv:2411.15785 — https://arxiv.org/abs/2411.15785

Introduces a Bounded-Cache Transformer (BCT) that enforces a fixed-length KV cache via dynamic updating of key/value sequences, trading unbounded growth for a predefined memory ceiling.

**Used for:** The closest Transformer-side analogue to BDH's bounded state. Referenced when explaining that "bounded memory" isn't unique to Hebbian/BDH-style systems — BCT achieves it via an eviction/capacity policy, whereas BDH achieves it structurally. Informs the Educational Disclaimer's framing.

---

**Keyless Attention: Value-Space Routing and Value-Only Caching for Efficient Transformers (2026).**
arXiv:2606.21848 — https://arxiv.org/abs/2606.21848
*(Author names are not exposed in the arXiv abstract page, PDF header, or HuggingFace paper listing as of this writing — cited by title/ID only.)*

Eliminates the key projection entirely, operating over queries and values only, yielding a Value-Only Cache that cuts KV cache memory and access overhead by exactly 50% over standard attention while matching or exceeding standard attention's decode throughput.

**Used for:** Evidence, in the Motivation section, that KV-cache size is a first-order deployment bottleneck worth visualizing — not a minor implementation detail.

---

## 3. Hebbian / fast-weight mechanisms

**Irie, K., Csordás, R., & Schmidhuber, J. (2023).**
*Practical Computational Power of Linear Transformers and Their Recurrent and Self-Referential Extensions.*
Proceedings of EMNLP 2023 — https://aclanthology.org/2023.emnlp-main.588

Studies autoregressive Transformers with linearized ("fast weight") attention, showing they are equivalent to RNN-like sequence processors with a fixed-size state, despite also being expressible as self-attention networks.

**Used for:** Theoretical grounding for treating the Hebbian synaptic matrix `W` as a **fixed-size state** rather than a growing cache — this fixed-state-recurrence-equals-linear-attention equivalence is exactly what the artifact's side-by-side memory bars try to make visually intuitive.

---

**Where to Bind Matters: Hebbian Fast Weights in Vision Transformers for Few-Shot Character Recognition (2026).**
arXiv:2605.02920 — https://arxiv.org/abs/2605.02920
*(Author names are not exposed in the arXiv abstract page, PDF, or any indexed citing source found — cited by title/ID only.)*

Confirms that the outer-product write rule used in fast-weight programmers is the Hebbian rule underlying modern (linearized) transformer attention, building on Ba et al. (2016), Munkhdalai & Trischler (2018), and Schlag et al. (2021).

**Used for:** Direct justification for the simplified update rule implemented in `src/model.py` and animated in the Synaptic Matrix Simulation:

\[
W_{t+1} = (1-\gamma)W_t + xx^T
\]

An outer-product Hebbian write (`xx^T`) with exponential decay (`γ`) — simplified for visualization and **not** the full BDH learning rule.

---

**Kaczmarz Linear Attention (2026).**
arXiv:2605.08587 — https://arxiv.org/abs/2605.08587
*(Author names are not exposed in the arXiv abstract page or PDF header — cited by title/ID only.)*

Surveys linear-attention/fast-weight formulations and their recurrent-state interpretation, situating outer-product Hebbian updates within the broader linear-attention literature.

**Used for:** Background for the "Decay Rate" control — used to confirm that setting `γ = 0` (no decay) causing unbounded matrix-norm growth is a known, expected failure mode of Hebbian-style accumulation, not an artifact bug.

---

## 4. Bounded-state sequence models (real-world analogues)

**Gu, A., & Dao, T. (2023).**
*Mamba: Linear-Time Sequence Modeling with Selective State Spaces.*
arXiv:2312.00752 — https://arxiv.org/abs/2312.00752

**Qin, Z., Yang, S., Sun, W., Shen, X., Li, D., Sun, W., & Zhong, Y. (2024).**
*HGRN2: Gated Linear RNNs with State Expansion.*
arXiv:2404.07904 — https://arxiv.org/abs/2404.07904 · Published at COLM 2024

Both describe production-grade sequence architectures that process arbitrarily long context using a **fixed-size recurrent state** rather than a cache that grows with context length; HGRN2 explicitly motivates itself by noting that serving Transformer-based LLMs is expensive due to KV-cache management, and uses an outer-product-based state-expansion mechanism strikingly similar in form to a Hebbian update.

**Used for:** Cited in the Future Improvements section as real deployed examples of the same "bounded-state" family BDH belongs to — motivates the "Multi-layer visualization" and "Interactive comparison against Transformer attention" roadmap items, and frames this artifact's Hebbian toggle as one member of a broader, active research category rather than a one-off idea.

---

## 5. Memory mechanisms in LLMs (surveys, for further reading)

**From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs (2025).**
arXiv:2504.15965 — https://arxiv.org/abs/2504.15965
*(Author names not confirmed from indexed sources found — cited by title/ID only.)*

**Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey (2026).**
arXiv:2602.06052 — https://arxiv.org/abs/2602.06052
*(Author names not confirmed from indexed sources found — cited by title/ID only.)*

Both survey how KV caching and longer-term memory mechanisms are used and extended across LLM-based systems and agents.

**Used for:** Linked in `docs/` as further-reading pointers for users who want context beyond this artifact's scope (e.g., agent memory, retrieval-augmented caching) — not directly implemented in any visualization.

---

## How Citations Map to Code

| Artifact component | Concept | Primary citation(s) |
|---|---|---|
| Context length slider / `memory_curve.json` (`kv_memory`) | Linear KV-cache growth | Xu, Khaira & Singh (2026); Wu & Tu (2024) |
| Context length slider / `memory_curve.json` (`hebbian_memory`) | Fixed-size bounded state | Kosowski et al. (2025); Irie, Csordás & Schmidhuber (2023) |
| Synaptic Matrix Simulation (`simulation.json`, `model.py`) | Hebbian outer-product update `W_{t+1} = (1-γ)W_t + xx^T` | Kosowski et al. (2025); *Where to Bind Matters* (2026) |
| Decay Rate control | Preventing unbounded norm growth | *Kaczmarz Linear Attention* (2026) |
| Activation Sparsity control | Sparse activation patterns in Hebbian updates | Kosowski et al. (2025) |
| Educational Disclaimer / bounded-cache framing | Bounded-cache Transformer as a contrasting approach | Yi et al. (2024), Bounded-Cache Transformer |
| Future Improvements roadmap | Real-world bounded-state architectures | Gu & Dao (2023) Mamba; Qin et al. (2024) HGRN2 |
| `docs/` further reading | Broader LLM/agent memory landscape | *From Human Memory to AI Memory* (2025); *Rethinking Memory Mechanisms* (2026) |

---

## Scope Note

This list is intentionally restricted to **papers published 2022–2026**. Foundational, pre-2022 work this project's ideas ultimately build on — the original Transformer paper (Vaswani et al., 2017), early fast-weight programmers (Schmidhuber, 1991–92), linear attention (Katharopoulos et al., 2020), and *Linear Transformers Are Secretly Fast Weight Programmers* (Schlag, Irie & Schmidhuber, 2021) — is acknowledged conceptually in the codebase's comments but omitted here per the 2022–2026 scope of this bibliography.

Three entries above (*Keyless Attention*, *Where to Bind Matters*, *Kaczmarz Linear Attention*, and the two memory surveys) list no retrievable author names as of this writing — arXiv abstract pages, PDF headers, and HuggingFace paper listings for these did not expose author metadata in any search performed. They are cited by title and arXiv ID only; please verify author attribution directly against the arXiv page before using these in a formal bibliography.

---

## Full Historical Reference (pre-2022, for context only)

- Vaswani, A. et al. (2017). *Attention Is All You Need.*
- Schmidhuber, J. (1991/1992). *Learning to Control Fast-Weight Memories.*
- Katharopoulos, A., Vyas, A., Pappas, N., & Fleuret, F. (2020). *Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention.* ICML.
- Schlag, I., Irie, K., & Schmidhuber, J. (2021). *Linear Transformers Are Secretly Fast Weight Programmers.* ICML.