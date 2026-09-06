# Third-Party Licenses

This file documents the licenses of third-party software used by this project. It does not change or replace the licenses of those projects.

This project's own code and documentation are licensed under the terms in `LICENSE`. The table below lists the third-party software this project depends on, each of which remains under its own license — nothing here relicenses those projects.

This project is inspired by the paper:

"The Dragon Hatchling: Learning to Reason with Structured Memory"
(arXiv:2509.26507)

The repository does not redistribute the paper, its figures, or its source code. The paper is cited for academic attribution only. Users should consult the original publication for the complete algorithm, theoretical analysis, and any applicable reuse terms.

| Dependency | Used in | License | License text |
|---|---|---|---|
| NumPy | `src/model.py`, `src/simulation.py` | BSD 3-Clause | https://github.com/numpy/numpy/blob/main/LICENSE.txt |
| Matplotlib | `notebooks/toy_model.ipynb` (plots) | Matplotlib License (BSD-compatible) | https://matplotlib.org/stable/project/license.html |
| Python standard library (`json`, `pathlib`, `sys`) | `src/utils.py` and throughout | Python Software Foundation License | https://docs.python.org/3/license.html |
| Jupyter Notebook / IPython | Notebook execution environment | BSD 3-Clause | https://jupyter.org/governance/projectlicense.html |

## Why this file exists separately from `LICENSE`

`LICENSE` states the terms under which *this project's own* code and docs may be reused. `licenses.md` instead documents the terms under which the *dependencies this project relies on* may be redistributed. Keeping them separate avoids implying that this project has any authority to relicense NumPy, Matplotlib, or any other third-party package.

## BDH / the source paper

The Dragon Hatchling (BDH) paper that motivates this project (arXiv:2509.26507) is cited, not redistributed — no text, figures, or code from that paper are included in this repository. See `citations.md` and `paper.md` for details, and consult the paper directly (https://arxiv.org/abs/2509.26507) for its own terms of reuse.

## Updating this file

If you add a new dependency (e.g., a frontend charting library inside `artifact/`), add a row here with its license type and a link to the license text, so the list stays accurate as the project grows.