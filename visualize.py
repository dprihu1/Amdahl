"""
Visualization module for Amdahl's Law performance analysis.

This module generates matplotlib plots showing speedup, efficiency, and
execution time scaling behavior across different processor counts.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Docker compatibility
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Any
import numpy as np


def plot_speedup(processor_counts: np.ndarray, speedups: np.ndarray, 
                 f: float, output_path: Path) -> None:
    """
    Generate a plot showing speedup vs. number of processors.

    Args:
        processor_counts: Array of processor counts.
        speedups: Array of speedup values corresponding to each processor count.
        f: Sequential fraction used in the calculation.
        output_path: Path where the plot will be saved.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(processor_counts, speedups, 'b-', linewidth=2, marker='o', markersize=4)
    plt.xlabel('Number of Processors', fontsize=12, fontweight='bold')
    plt.ylabel('Speedup (S_p)', fontsize=12, fontweight='bold')
    plt.title(f'Speedup vs. Number of Processors (f = {f})', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlim(0, processor_counts[-1] + processor_counts[-1] * 0.05)
    plt.tight_layout()
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_efficiency(processor_counts: np.ndarray, efficiencies: np.ndarray,
                    f: float, output_path: Path) -> None:
    """
    Generate a plot showing efficiency vs. number of processors.

    Args:
        processor_counts: Array of processor counts.
        efficiencies: Array of efficiency values corresponding to each processor count.
        f: Sequential fraction used in the calculation.
        output_path: Path where the plot will be saved.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(processor_counts, efficiencies, 'g-', linewidth=2, marker='s', markersize=4)
    plt.xlabel('Number of Processors', fontsize=12, fontweight='bold')
    plt.ylabel('Efficiency (E_p)', fontsize=12, fontweight='bold')
    plt.title(f'Efficiency vs. Number of Processors (f = {f})', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlim(0, processor_counts[-1] + processor_counts[-1] * 0.05)
    plt.ylim(0, max(efficiencies) * 1.1)
    plt.tight_layout()
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_execution_time(processor_counts: np.ndarray, time_ratios: np.ndarray,
                       f: float, output_path: Path) -> None:
    """
    Generate a plot showing execution time ratio vs. number of processors.

    Args:
        processor_counts: Array of processor counts.
        time_ratios: Array of execution time ratios (T_p / T_1).
        f: Sequential fraction used in the calculation.
        output_path: Path where the plot will be saved.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(processor_counts, time_ratios, 'r-', linewidth=2, marker='^', markersize=4)
    plt.xlabel('Number of Processors', fontsize=12, fontweight='bold')
    plt.ylabel('Execution Time Ratio (T_p / T_1)', fontsize=12, fontweight='bold')
    plt.title(f'Execution Time Ratio vs. Number of Processors (f = {f})', 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlim(0, processor_counts[-1] + processor_counts[-1] * 0.05)
    plt.tight_layout()
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_all(simulation_results: Dict[str, Any], f: float, output_dir: Path) -> None:
    """
    Generate all three performance plots and save them to the output directory.

    Creates three PNG files:
    - speedup.png
    - efficiency.png
    - execution_time.png

    Args:
        simulation_results: Dictionary containing 'processors', 'speedups',
                           'efficiencies', and 'time_ratios' arrays.
        f: Sequential fraction used in the calculation.
        output_dir: Directory where plots will be saved.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    processors = simulation_results['processors']
    speedups = simulation_results['speedups']
    efficiencies = simulation_results['efficiencies']
    time_ratios = simulation_results['time_ratios']

    # Generate all three plots
    plot_speedup(processors, speedups, f, output_dir / 'speedup.png')
    plot_efficiency(processors, efficiencies, f, output_dir / 'efficiency.png')
    plot_execution_time(processors, time_ratios, f, output_dir / 'execution_time.png')

