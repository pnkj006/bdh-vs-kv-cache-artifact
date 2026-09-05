"""
utils.py
=========

Shared utility functions used throughout the project.

This module contains helper functions only.
No simulation logic should live here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import json
import numpy as np


# ============================================================
# Directory Helpers
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"

PRECOMPUTED_DIR = ROOT / "artifact" / "precomputed"


def ensure_directory(path: Path) -> None:
    """
    Create directory if it does not exist.
    """

    path.mkdir(parents=True, exist_ok=True)


# ============================================================
# JSON Helpers
# ============================================================

def save_json(data: Any, filepath: Path) -> None:
    """
    Save dictionary/list to JSON.
    """

    ensure_directory(filepath.parent)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(filepath: Path):
    """
    Load JSON file.
    """

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Matrix Utilities
# ============================================================

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Normalize matrix to [-1,1].
    """

    max_abs = np.max(np.abs(matrix))

    if max_abs == 0:
        return matrix.copy()

    return matrix / max_abs


def matrix_density(matrix: np.ndarray) -> float:
    """
    Fraction of non-zero entries.
    """

    return float(np.count_nonzero(matrix) / matrix.size)


def frobenius_norm(matrix: np.ndarray) -> float:
    """
    Frobenius norm.
    """

    return float(np.linalg.norm(matrix))


# ============================================================
# Statistics
# ============================================================

def summary_statistics(values):
    """
    Basic statistics for a sequence.
    """

    values = np.asarray(values)

    return {
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
    }


# ============================================================
# Memory Conversion
# ============================================================

def bytes_to_kib(x: int) -> float:
    return x / 1024


def bytes_to_mib(x: int) -> float:
    return x / (1024 ** 2)


def bytes_to_gib(x: int) -> float:
    return x / (1024 ** 3)


# ============================================================
# Random Utilities
# ============================================================

def get_rng(seed: int | None = None):
    """
    Consistent random number generator.
    """

    return np.random.default_rng(seed)


# ============================================================
# Validation
# ============================================================

def validate_probability(value: float, name: str):
    """
    Validate probability in [0,1].
    """

    if not (0.0 <= value <= 1.0):
        raise ValueError(
            f"{name} must be between 0 and 1."
        )


def validate_positive(value: int | float, name: str):
    """
    Validate positive number.
    """

    if value <= 0:
        raise ValueError(
            f"{name} must be positive."
        )


# ============================================================
# Export Helpers
# ============================================================

def export_precomputed(
    filename: str,
    data: dict,
):
    """
    Save precomputed artifact JSON.

    Example
    -------
    export_precomputed(
        "memory_curve.json",
        curve
    )
    """

    ensure_directory(PRECOMPUTED_DIR)

    save_json(
        data,
        PRECOMPUTED_DIR / filename,
    )


# ============================================================
# Console Formatting
# ============================================================

def print_header(title: str):

    line = "=" * len(title)

    print("\n" + line)

    print(title)

    print(line)


def print_success(message: str):
    print(f"[✓] {message}")


def print_warning(message: str):
    print(f"[!] {message}")


# ============================================================
# Timer
# ============================================================

from time import perf_counter


class Timer:
    """
    Simple context manager.

    Example
    -------
    with Timer("Simulation"):
        ...
    """

    def __init__(self, name="Task"):

        self.name = name

    def __enter__(self):

        self.start = perf_counter()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        elapsed = perf_counter() - self.start

        print(f"{self.name}: {elapsed:.3f} sec")


# ============================================================
# Module Test
# ============================================================

if __name__ == "__main__":

    print_header("Utils Test")

    rng = get_rng(42)

    matrix = rng.normal(size=(8, 8))

    print(summary_statistics(matrix))

    print(matrix_density(matrix))

    print(frobenius_norm(matrix))

    print_success("Utilities loaded successfully.")