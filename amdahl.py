"""
Core computation module for Amdahl's Law performance analysis.

This module implements the mathematical formulas for calculating speedup,
efficiency, and execution time ratios according to Amdahl's Law.
"""

import numpy as np
from typing import Tuple, Dict, Any


def calculate_speedup(f: float, p: int) -> float:
    """
    Calculate the speedup according to Amdahl's Law.

    Amdahl's Law states that the maximum speedup achievable is limited by
    the sequential fraction of the program. The formula is:
        S_p = 1 / (f + (1 - f) / p)

    where:
        S_p = Speedup with p processors
        f = Fraction of the program that is sequential (0 <= f <= 1)
        p = Number of processors (p >= 1)

    Args:
        f: Fraction of the program that is sequential (between 0 and 1).
        p: Number of processors (must be >= 1).

    Returns:
        The speedup S_p achieved with p processors.

    Raises:
        ValueError: If f is not in [0, 1] or p is less than 1.
    """
    if not (0 <= f <= 1):
        raise ValueError(f"Sequential fraction f must be in [0, 1], got {f}")
    if p < 1:
        raise ValueError(f"Number of processors p must be >= 1, got {p}")

    # Avoid division by zero when f = 1 (fully sequential)
    if f == 1:
        return 1.0

    # Amdahl's Law: S_p = 1 / (f + (1 - f) / p)
    denominator = f + (1 - f) / p
    return 1.0 / denominator


def calculate_efficiency(f: float, p: int) -> float:
    """
    Calculate the efficiency of parallel execution.

    Efficiency measures how well the processors are utilized and is defined as:
        E_p = S_p / p

    where:
        E_p = Efficiency with p processors
        S_p = Speedup with p processors
        p = Number of processors

    Args:
        f: Fraction of the program that is sequential (between 0 and 1).
        p: Number of processors (must be >= 1).

    Returns:
        The efficiency E_p achieved with p processors.

    Raises:
        ValueError: If f is not in [0, 1] or p is less than 1.
    """
    speedup = calculate_speedup(f, p)
    return speedup / p


def calculate_execution_time_ratio(f: float, p: int) -> float:
    """
    Calculate the execution time ratio (T_p / T_1).

    The execution time ratio represents how much faster the program runs
    compared to single-processor execution:
        T_p = T_1 / S_p

    which means:
        T_p / T_1 = 1 / S_p

    Args:
        f: Fraction of the program that is sequential (between 0 and 1).
        p: Number of processors (must be >= 1).

    Returns:
        The execution time ratio (T_p / T_1), where smaller values indicate
        better performance.

    Raises:
        ValueError: If f is not in [0, 1] or p is less than 1.
    """
    speedup = calculate_speedup(f, p)
    return 1.0 / speedup


def simulate_scaling(f: float, max_procs: int) -> Dict[str, np.ndarray]:
    """
    Simulate performance scaling over a range of processor counts.

    This function calculates speedup, efficiency, and execution time ratios
    for all processor counts from 1 to max_procs, allowing for visualization
    and analysis of scaling behavior.

    Args:
        f: Fraction of the program that is sequential (between 0 and 1).
        max_procs: Maximum number of processors to simulate (must be >= 1).

    Returns:
        A dictionary containing:
            - 'processors': Array of processor counts from 1 to max_procs
            - 'speedups': Array of speedup values for each processor count
            - 'efficiencies': Array of efficiency values for each processor count
            - 'time_ratios': Array of execution time ratios for each processor count

    Raises:
        ValueError: If f is not in [0, 1] or max_procs is less than 1.
    """
    if not (0 <= f <= 1):
        raise ValueError(f"Sequential fraction f must be in [0, 1], got {f}")
    if max_procs < 1:
        raise ValueError(f"Maximum processors must be >= 1, got {max_procs}")

    # Create array of processor counts [1, 2, ..., max_procs]
    processors = np.arange(1, max_procs + 1, dtype=np.int32)

    # Vectorized computation using NumPy for efficiency
    # For f = 1 (fully sequential), speedup is always 1.0
    if f == 1:
        speedups = np.ones(max_procs, dtype=np.float64)
    else:
        # Amdahl's Law: S_p = 1 / (f + (1 - f) / p)
        # Vectorized over all processor counts
        denominator = f + (1 - f) / processors.astype(np.float64)
        speedups = 1.0 / denominator

    # Efficiency: E_p = S_p / p
    efficiencies = speedups / processors

    # Execution time ratio: T_p / T_1 = 1 / S_p
    time_ratios = 1.0 / speedups

    return {
        'processors': processors,
        'speedups': speedups,
        'efficiencies': efficiencies,
        'time_ratios': time_ratios
    }

