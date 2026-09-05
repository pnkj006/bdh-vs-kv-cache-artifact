"""
evaluation.py
=============

Evaluation utilities for the educational artifact.

This module measures whether the simplified Hebbian proxy behaves
as expected. It does NOT evaluate the BDH architecture itself.

Responsibilities
----------------
- Norm evolution
- Saturation detection
- Memory validation
- Parameter sweep evaluation
- Summary statistics

No plotting.
No visualization.
No JSON export.
"""

from __future__ import annotations

from typing import Dict

import numpy as np

from model import (
    HebbianConfig,
    HebbianMemory,
    compare_memory,
    random_sparse_pattern,
)

from simulation import (
    SimulationConfig,
    simulate_sequence,
)


# ============================================================
# Norm Evaluation
# ============================================================

def evaluate_norm_growth(
    hebbian_cfg: HebbianConfig,
    sim_cfg: SimulationConfig,
) -> Dict:
    """
    Evaluate Frobenius norm evolution.
    """

    result = simulate_sequence(
        hebbian_cfg,
        sim_cfg,
    )

    norms = np.asarray(result["norms"])

    return {
        "initial_norm": float(norms[0]),
        "final_norm": float(norms[-1]),
        "maximum_norm": float(np.max(norms)),
        "minimum_norm": float(np.min(norms)),
        "mean_norm": float(np.mean(norms)),
        "std_norm": float(np.std(norms)),
    }


# ============================================================
# Saturation Detection
# ============================================================

def detect_saturation(
    hebbian_cfg: HebbianConfig,
    sim_cfg: SimulationConfig,
    tolerance: float = 1e-3,
):
    """
    Detect whether the norm stabilizes.
    """

    result = simulate_sequence(
        hebbian_cfg,
        sim_cfg,
    )

    norms = np.asarray(result["norms"])

    window = min(20, len(norms))

    recent = norms[-window:]

    saturated = np.std(recent) < tolerance

    return {
        "saturated": saturated,
        "recent_std": float(np.std(recent)),
        "recent_mean": float(np.mean(recent)),
    }


# ============================================================
# Weight Statistics
# ============================================================

def evaluate_weights(
    hebbian_cfg: HebbianConfig,
    sim_cfg: SimulationConfig,
):
    """
    Evaluate final synaptic matrix.
    """

    result = simulate_sequence(
        hebbian_cfg,
        sim_cfg,
    )

    matrix = np.asarray(
        result["frames"][-1]["matrix"]
    )

    return {
        "max_weight": float(np.max(matrix)),
        "min_weight": float(np.min(matrix)),
        "mean_weight": float(np.mean(matrix)),
        "std_weight": float(np.std(matrix)),
        "active_connections": int(np.count_nonzero(matrix)),
        "density": float(
            np.count_nonzero(matrix) / matrix.size
        ),
    }


# ============================================================
# Memory Validation
# ============================================================

def validate_memory_scaling(
    hebbian_cfg: HebbianConfig,
):
    """
    Compare KV-cache and Hebbian memory.

    Hebbian memory should remain constant.
    """

    model = HebbianMemory(hebbian_cfg)

    lengths = [
        128,
        512,
        2048,
        8192,
        32768,
    ]

    stats = []

    for seq in lengths:

        result = compare_memory(
            sequence_length=seq,
            hidden_size=768,
            n_layers=12,
            hebbian_model=model,
        )

        stats.append(result)

    hebb = [x["hebbian_bytes"] for x in stats]

    constant = len(set(hebb)) == 1

    return {
        "memory_scaling_valid": constant,
        "results": stats,
    }


# ============================================================
# Decay Study
# ============================================================

def evaluate_decay(
    decay_values,
):
    """
    Observe decay effect on final norm.
    """

    outputs = []

    sim_cfg = SimulationConfig()

    for d in decay_values:

        cfg = HebbianConfig(
            decay=d,
        )

        result = evaluate_norm_growth(
            cfg,
            sim_cfg,
        )

        outputs.append(
            {
                "decay": d,
                "final_norm": result["final_norm"],
            }
        )

    return outputs


# ============================================================
# Sparsity Study
# ============================================================

def evaluate_sparsity(
    sparsities,
):
    """
    Observe sparsity effect.
    """

    outputs = []

    sim_cfg = SimulationConfig()

    for s in sparsities:

        cfg = HebbianConfig(
            sparsity=s,
        )

        result = evaluate_weights(
            cfg,
            sim_cfg,
        )

        outputs.append(
            {
                "sparsity": s,
                "density": result["density"],
                "active_connections":
                result["active_connections"],
            }
        )

    return outputs


# ============================================================
# Overall Evaluation
# ============================================================

def full_evaluation():
    """
    Runs all evaluations.
    """

    hebbian_cfg = HebbianConfig()

    sim_cfg = SimulationConfig()

    return {
        "norm_growth":
        evaluate_norm_growth(
            hebbian_cfg,
            sim_cfg,
        ),

        "saturation":
        detect_saturation(
            hebbian_cfg,
            sim_cfg,
        ),

        "weights":
        evaluate_weights(
            hebbian_cfg,
            sim_cfg,
        ),

        "memory":
        validate_memory_scaling(
            hebbian_cfg,
        ),

        "decay":
        evaluate_decay(
            [0.0, 0.01, 0.05, 0.10],
        ),

        "sparsity":
        evaluate_sparsity(
            [0.05, 0.10, 0.20, 0.40],
        ),
    }


# ============================================================
# Module Test
# ============================================================

if __name__ == "__main__":

    results = full_evaluation()

    print("\n=== Evaluation Summary ===\n")

    for key, value in results.items():

        print(f"{key}")

        print(value)

        print()