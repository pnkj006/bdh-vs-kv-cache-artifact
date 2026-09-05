"""
model.py
========

Core computational model for the educational artifact:

"Hebbian vs. KV-Cache Memory"

IMPORTANT
---------
This is **NOT** an implementation of the BDH architecture described in
Kosowski et al. (2025).

The Hebbian update implemented here is an intentionally simplified
pedagogical proxy used only for interactive visualization.

The real BDH update rule must be cited directly from the paper whenever
the artifact discusses BDH-specific equations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


# ============================================================
# Configuration
# ============================================================

@dataclass
class HebbianConfig:
    """
    Configuration for the simplified Hebbian memory.

    Parameters
    ----------
    n_neurons
        Size of synaptic memory matrix.

    decay
        Exponential decay coefficient.

    learning_rate
        Hebbian learning rate.

    sparsity
        Fraction of neurons activated per token.
    """

    n_neurons: int = 64
    decay: float = 0.05
    learning_rate: float = 0.10
    sparsity: float = 0.15


# ============================================================
# Token Encoding
# ============================================================

def random_sparse_pattern(
    n_neurons: int,
    sparsity: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    Generates a sparse bipolar activation vector.

    Returns
    -------
    ndarray
        Shape (n_neurons,)
        Values in {-1,0,+1}
    """

    if rng is None:
        rng = np.random.default_rng()

    pattern = np.zeros(n_neurons)

    active = max(1, int(sparsity * n_neurons))

    idx = rng.choice(n_neurons, active, replace=False)

    signs = rng.choice([-1.0, 1.0], active)

    pattern[idx] = signs

    return pattern


# ============================================================
# Hebbian Memory
# ============================================================

class HebbianMemory:
    """
    Simplified fixed-size Hebbian memory.

    Memory is represented by a fixed NxN synaptic matrix.
    """

    def __init__(self, config: HebbianConfig):

        self.config = config

        self.W = np.zeros(
            (
                config.n_neurons,
                config.n_neurons,
            ),
            dtype=np.float32,
        )

    def reset(self):
        """Clear memory."""

        self.W.fill(0.0)

    def update(self, activity: np.ndarray):
        """
        Simplified Hebbian update.

        W <- (1-d)W + lr * x x^T

        NOTE:
        This is NOT the BDH update.
        """

        outer = np.outer(activity, activity)

        self.W *= (1.0 - self.config.decay)

        self.W += self.config.learning_rate * outer

    def frobenius_norm(self) -> float:
        """Return Frobenius norm."""

        return float(np.linalg.norm(self.W))

    def memory_bytes(self) -> int:
        """
        Physical memory used by synaptic matrix.
        """

        return self.W.nbytes

    def snapshot(self) -> np.ndarray:
        """Copy of current matrix."""

        return self.W.copy()


# ============================================================
# KV Cache Memory
# ============================================================

def kv_cache_memory_bytes(
    sequence_length: int,
    hidden_size: int,
    n_layers: int,
    dtype_bytes: int = 2,
) -> int:
    """
    Exact KV-cache storage.

    Memory =
        sequence_length
        × n_layers
        × hidden_size
        × 2
        × dtype_bytes

    Factor 2 = Keys + Values.
    """

    return (
        sequence_length
        * n_layers
        * hidden_size
        * 2
        * dtype_bytes
    )


def bytes_to_kib(x: int) -> float:
    return x / 1024


def bytes_to_mib(x: int) -> float:
    return x / (1024 ** 2)


def bytes_to_gib(x: int) -> float:
    return x / (1024 ** 3)


# ============================================================
# Public API
# ============================================================

def simulate_single_token(
    model: HebbianMemory,
    rng: np.random.Generator | None = None,
) -> Tuple[np.ndarray, float]:
    """
    Advance memory by one synthetic token.

    Returns
    -------
    matrix
        Updated synaptic matrix.

    norm
        Frobenius norm.
    """

    x = random_sparse_pattern(
        model.config.n_neurons,
        model.config.sparsity,
        rng,
    )

    model.update(x)

    return (
        model.snapshot(),
        model.frobenius_norm(),
    )


def compare_memory(
    sequence_length: int,
    hidden_size: int,
    n_layers: int,
    hebbian_model: HebbianMemory,
) -> dict:
    """
    Returns memory statistics for the artifact.
    """

    kv = kv_cache_memory_bytes(
        sequence_length,
        hidden_size,
        n_layers,
    )

    hebb = hebbian_model.memory_bytes()

    return {
        "sequence_length": sequence_length,
        "kv_bytes": kv,
        "kv_kib": bytes_to_kib(kv),
        "kv_mib": bytes_to_mib(kv),
        "kv_gib": bytes_to_gib(kv),
        "hebbian_bytes": hebb,
        "hebbian_kib": bytes_to_kib(hebb),
        "hebbian_norm": hebbian_model.frobenius_norm(),
    }


# ============================================================
# Example
# ============================================================

if __name__ == "__main__":

    cfg = HebbianConfig(
        n_neurons=64,
        decay=0.05,
        learning_rate=0.1,
        sparsity=0.10,
    )

    model = HebbianMemory(cfg)

    rng = np.random.default_rng(42)

    for _ in range(10):
        simulate_single_token(model, rng)

    stats = compare_memory(
        sequence_length=8192,
        hidden_size=768,
        n_layers=12,
        hebbian_model=model,
    )

    print(stats)