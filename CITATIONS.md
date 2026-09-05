# Citations

This project draws on external work in two ways: the conceptual motivation for the toy model, and the open-source libraries used to build it. Both are listed here so every non-original idea or piece of software in the repository can be traced to its source.

## Conceptual / research citations

**Primary inspiration:**

Pathway, "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain" (Baby Dragon Hatchling / BDH), arXiv:2509.26507, 2025.
https://arxiv.org/abs/2509.26507

This paper's contrast between a Transformer's growing KV-cache and a fixed-size, Hebbian-updated synaptic memory is the single idea this project visualizes. No text, figures, code, or results from the paper are reproduced here — see `paper.md` for a fuller summary and `limitations.md` for what is and isn't reproduced from it.

**Background reading used while writing the documentation** (secondary coverage of the same paper, consulted for context only, not as a technical source):

- Pathway project page / GitHub repository for "bdh" (Baby Dragon Hatchling).
- Public write-ups and summaries of the BDH architecture published after the paper's release (used only to cross-check the plain-language description in `paper.md`, not for any technical detail implemented in code).

## Software / library citations

| Library | Used for | License |
|---|---|---|
| NumPy | Matrix operations in `model.py` / `simulation.py` | BSD 3-Clause |
| Matplotlib | Plots inside `toy_model.ipynb` | Matplotlib License (BSD-style) |
| Python standard library (`json`, `pathlib`, `sys`) | I/O and path handling in `utils.py` | PSF License |
| Jupyter / IPython | Notebook execution environment | BSD 3-Clause |

Full license text for each dependency is in `licenses.md`; the project's own license is in `LICENSE`.

## Data

No external datasets are used. All token activations processed by the toy model are synthetically generated at runtime (`random_sparse_pattern`, seeded with `random_seed=42`) and do not originate from any third-party corpus, so no data citation is required.

## How to cite this project

If you build on this repository for the hackathon or afterward, please cite it alongside the BDH paper above, since the entire toy model exists to illustrate one of that paper's ideas — this project is a teaching aid built on top of that work, not an independent result.