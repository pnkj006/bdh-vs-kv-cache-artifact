"""
simulation.py
=============

Simulation engine for the educational artifact.

This module builds on model.py and is responsible for:

1. Token-by-token simulation
2. Parameter sweeps
3. Animation frame generation
4. Export-ready data structures

No visualization code belongs here.
No plotting.
No HTML.
No JSON writing.

Those are handled elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from model import (
    HebbianConfig,
    HebbianMemory,
    compare_memory,
    random_sparse_pattern,
)


# ============================================================
# Simulation Configuration
# ============================================================

@dataclass
class SimulationConfig:

    n_tokens: int = 256

    random_seed: int = 42

    hidden_size: int = 768

    n_layers: int = 12


# ============================================================
# Token Simulation
# ============================================================

def simulate_sequence(
    hebbian_cfg: HebbianConfig,
    sim_cfg: SimulationConfig,
):
    """
    Runs token-by-token simulation.

    Returns
    -------
    dict
    """

    rng = np.random.default_rng(sim_cfg.random_seed)

    model = HebbianMemory(hebbian_cfg)

    frames = []

    norms = []

    for step in range(sim_cfg.n_tokens):

        activity = random_sparse_pattern(
            hebbian_cfg.n_neurons,
            hebbian_cfg.sparsity,
            rng,
        )

        model.update(activity)

        norm = model.frobenius_norm()

        norms.append(norm)

        frames.append(
            {
                "step": step + 1,
                "matrix": model.snapshot().tolist(),
                "norm": norm,
            }
        )

    return {
        "frames": frames,
        "norms": norms,
    }


# ============================================================
# Memory Curve
# ============================================================

def generate_memory_curve(
    hebbian_cfg: HebbianConfig,
    hidden_size: int,
    n_layers: int,
    max_tokens: int = 131072,
    step: int = 512,
):
    """
    Computes KV-cache vs Hebbian memory.
    """

    model = HebbianMemory(hebbian_cfg)

    tokens = []

    kv = []

    hebb = []

    for t in range(step, max_tokens + step, step):

        stats = compare_memory(
            sequence_length=t,
            hidden_size=hidden_size,
            n_layers=n_layers,
            hebbian_model=model,
        )

        tokens.append(t)

        kv.append(stats["kv_gib"])

        hebb.append(stats["hebbian_kib"])

    return {
        "tokens": tokens,
        "kv_memory": kv,
        "hebbian_memory": hebb,
    }


# ============================================================
# Parameter Sweep
# ============================================================

def sweep_decay(
    decay_values,
    base_cfg: HebbianConfig,
    sim_cfg: SimulationConfig,
):
    """
    Sweep decay values.
    """

    results = []

    for decay in decay_values:

        cfg = HebbianConfig(
            n_neurons=base_cfg.n_neurons,
            learning_rate=base_cfg.learning_rate,
            sparsity=base_cfg.sparsity,
            decay=decay,
        )

        sim = simulate_sequence(cfg, sim_cfg)

        results.append(
            {
                "decay": decay,
                "final_norm": sim["norms"][-1],
            }
        )

    return results


def sweep_sparsity(
    sparsity_values,
    base_cfg,
    sim_cfg,
):

    results = []

    for s in sparsity_values:

        cfg = HebbianConfig(
            n_neurons=base_cfg.n_neurons,
            learning_rate=base_cfg.learning_rate,
            decay=base_cfg.decay,
            sparsity=s,
        )

        sim = simulate_sequence(cfg, sim_cfg)

        results.append(
            {
                "sparsity": s,
                "final_norm": sim["norms"][-1],
            }
        )

    return results


def sweep_neurons(
    neuron_values,
    base_cfg,
    sim_cfg,
):

    results = []

    for n in neuron_values:

        cfg = HebbianConfig(
            n_neurons=n,
            learning_rate=base_cfg.learning_rate,
            decay=base_cfg.decay,
            sparsity=base_cfg.sparsity,
        )

        sim = simulate_sequence(cfg, sim_cfg)

        results.append(
            {
                "neurons": n,
                "final_norm": sim["norms"][-1],
            }
        )

    return results


# ============================================================
# Frame Generator
# ============================================================

def generate_animation_frames(
    hebbian_cfg,
    sim_cfg,
):
    """
    Returns animation-ready frames.
    """

    sim = simulate_sequence(
        hebbian_cfg,
        sim_cfg,
    )

    return sim["frames"]


# ============================================================
# Dashboard Metrics
# ============================================================

def generate_metrics(
    hebbian_cfg,
    sim_cfg,
):
    """
    Generates summary metrics for UI.
    """

    sim = simulate_sequence(
        hebbian_cfg,
        sim_cfg,
    )

    final_matrix = np.array(
        sim["frames"][-1]["matrix"]
    )

    return {
        "tokens_processed": sim_cfg.n_tokens,
        "final_norm": sim["norms"][-1],
        "max_weight": float(np.max(final_matrix)),
        "min_weight": float(np.min(final_matrix)),
        "mean_weight": float(np.mean(final_matrix)),
        "active_synapses": int(np.count_nonzero(final_matrix)),
    }


# ============================================================
# Export Bundle
# ============================================================

def build_precomputed_bundle():

    hebb_cfg = HebbianConfig()

    sim_cfg = SimulationConfig()

    return {
        "memory_curve": generate_memory_curve(
            hebb_cfg,
            sim_cfg.hidden_size,
            sim_cfg.n_layers,
        ),
        "simulation": simulate_sequence(
            hebb_cfg,
            sim_cfg,
        ),
        "metrics": generate_metrics(
            hebb_cfg,
            sim_cfg,
        ),
    }


# ============================================================
# Example
# ============================================================

if __name__ == "__main__":

    bundle = build_precomputed_bundle()

    print(bundle.keys())

    print(
        bundle["memory_curve"].keys()
    )

    print(
        len(bundle["simulation"]["frames"])
    )