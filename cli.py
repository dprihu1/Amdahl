#!/usr/bin/env python3
"""
Command-line interface for the Amdahl's Law Performance Analyzer.

This module provides the main entry point for running performance analysis
via command-line arguments or configuration files.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

from amdahl import simulate_scaling
from visualize import plot_all
from utils import (
    validate_fraction,
    validate_processors,
    load_config,
    format_table,
    ensure_output_dir
)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments using argparse.

    Returns:
        Namespace object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Amdahl\'s Law Performance Analyzer - Calculate and visualize '
                    'parallel performance scaling according to Amdahl\'s Law.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --fraction 0.05 --max_procs 100
  python cli.py -f 0.1 -p 50 --output-dir ./results
  python cli.py --config config.yaml
  python cli.py --fraction 0.2 --max_procs 200 --no-plots
        """
    )

    parser.add_argument(
        '-f', '--fraction',
        type=float,
        help='Fraction of the program that is sequential (0 <= f <= 1)'
    )

    parser.add_argument(
        '-p', '--max_procs',
        type=int,
        help='Maximum number of processors to simulate (default: 100)'
    )

    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (YAML format). '
             'Command-line arguments override config file values.'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Directory where plots will be saved (default: ./output)'
    )

    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip generating plots (only compute and display table)'
    )

    return parser.parse_args()


def get_config_values(args: argparse.Namespace) -> Tuple[float, int, bool]:
    """
    Determine configuration values from command-line arguments and/or config file.

    Priority: Command-line arguments > Config file > Defaults

    Args:
        args: Parsed command-line arguments.

    Returns:
        Tuple of (fraction, max_procs, generate_plots).
    """
    config = {}
    
    # Load config file if provided
    if args.config:
        try:
            config_path = Path(args.config)
            if not config_path.is_absolute():
                config_path = Path.cwd() / config_path
            config = load_config(config_path)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading config file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Try to load default config.yaml if it exists
        try:
            config = load_config()
        except FileNotFoundError:
            pass  # Config file is optional

    # Get values (command-line args override config file)
    fraction = args.fraction
    if fraction is None:
        fraction = config.get('fraction')
        if fraction is None:
            parser = argparse.ArgumentParser()
            parser.error('Sequential fraction (-f/--fraction) is required. '
                        'Provide it via command-line argument or config file.')

    max_procs = args.max_procs
    if max_procs is None:
        max_procs = config.get('max_procs', 100)

    generate_plots = not args.no_plots
    if args.no_plots:
        generate_plots = False
    else:
        generate_plots = config.get('generate_plots', True)

    return fraction, max_procs, generate_plots


def main() -> None:
    """
    Main entry point for the CLI application.
    """
    args = parse_arguments()

    try:
        # Get configuration values
        fraction, max_procs, generate_plots = get_config_values(args)

        # Validate inputs
        validate_fraction(fraction)
        validate_processors(max_procs)

        # Run simulation
        print(f"\n{'='*70}")
        print(f"Amdahl's Law Performance Analysis")
        print(f"{'='*70}")
        print(f"Sequential Fraction (f): {fraction}")
        print(f"Maximum Processors: {max_procs}")
        print(f"{'='*70}\n")

        simulation_results = simulate_scaling(fraction, max_procs)

        # Display results table
        print("Performance Results:")
        print(format_table(simulation_results))
        print()

        # Generate plots if requested
        if generate_plots:
            output_dir = ensure_output_dir(Path(args.output_dir))
            print(f"Generating plots in: {output_dir.absolute()}")
            plot_all(simulation_results, fraction, output_dir)
            print("Plots generated successfully:")
            print(f"  - {output_dir / 'speedup.png'}")
            print(f"  - {output_dir / 'efficiency.png'}")
            print(f"  - {output_dir / 'execution_time.png'}")
        else:
            print("Plots generation skipped (--no-plots flag set)")

        print(f"\n{'='*70}")
        print("Analysis complete!")
        print(f"{'='*70}\n")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

