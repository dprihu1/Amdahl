"""
Utility functions for validation, configuration loading, and file operations.

This module provides helper functions used across the Amdahl's Law analyzer
for input validation, configuration management, and path handling.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def validate_fraction(f: float) -> None:
    """
    Validate that the sequential fraction is in the valid range [0, 1].

    Args:
        f: The sequential fraction to validate.

    Raises:
        ValueError: If f is not in [0, 1].
    """
    if not isinstance(f, (int, float)):
        raise ValueError(f"Sequential fraction must be a number, got {type(f).__name__}")
    if not (0 <= f <= 1):
        raise ValueError(f"Sequential fraction must be in [0, 1], got {f}")


def validate_processors(p: int) -> None:
    """
    Validate that the number of processors is valid (>= 1 and integer).

    Args:
        p: The number of processors to validate.

    Raises:
        ValueError: If p is less than 1 or not an integer.
    """
    if not isinstance(p, int):
        # Try to convert float to int if it's a whole number
        if isinstance(p, float) and p.is_integer():
            p = int(p)
        else:
            raise ValueError(f"Number of processors must be an integer, got {type(p).__name__}")
    if p < 1:
        raise ValueError(f"Number of processors must be >= 1, got {p}")


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    If no config path is provided, attempts to load from 'config.yaml'
    in the current working directory or project root.

    Args:
        config_path: Optional path to the configuration file. If None,
                    attempts to find 'config.yaml' in the current directory.

    Returns:
        A dictionary containing the configuration values.

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the config file is not valid YAML.
    """
    if config_path is None:
        # Try to find config.yaml relative to current working directory
        config_path = Path.cwd() / 'config.yaml'
        if not config_path.exists():
            # Try project root (where this script is located)
            project_root = Path(__file__).parent
            config_path = project_root / 'config.yaml'

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}. "
            "Please provide a valid config.yaml file or use command-line arguments."
        )

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    if config is None:
        config = {}

    return config


def format_table(results: Dict[str, Any]) -> str:
    """
    Format simulation results as an ASCII table for console output.

    This function prepares data for use with the 'tabulate' library,
    formatting processor counts, speedups, efficiencies, and time ratios
    into a readable table structure.

    Args:
        results: Dictionary containing 'processors', 'speedups',
                'efficiencies', and 'time_ratios' arrays.

    Returns:
        A formatted string representation of the results table.
    """
    from tabulate import tabulate

    processors = results['processors']
    speedups = results['speedups']
    efficiencies = results['efficiencies']
    time_ratios = results['time_ratios']

    # Prepare table data
    table_data = []
    for i in range(len(processors)):
        table_data.append([
            processors[i],
            f"{speedups[i]:.6f}",
            f"{efficiencies[i]:.6f}",
            f"{time_ratios[i]:.6f}"
        ])

    headers = ["Processors", "Speedup", "Efficiency", "Time Ratio"]
    return tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".6f")


def ensure_output_dir(output_path: Path) -> Path:
    """
    Ensure that an output directory exists, creating it if necessary.

    Args:
        output_path: Path to the output directory (can be relative or absolute).

    Returns:
        The absolute Path object for the output directory.
    """
    output_path = Path(output_path)

    # If path is relative, resolve it relative to current working directory
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    # Create directory and parents if they don't exist
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path

