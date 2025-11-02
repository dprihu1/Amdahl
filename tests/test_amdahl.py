"""
Unit tests for the Amdahl's Law computation module.

This test suite validates the correctness of all mathematical calculations
and input validation functions.
"""

import pytest
import numpy as np
from amdahl import (
    calculate_speedup,
    calculate_efficiency,
    calculate_execution_time_ratio,
    simulate_scaling
)


class TestCalculateSpeedup:
    """Test cases for calculate_speedup function."""

    def test_speedup_known_values(self):
        """Test speedup calculation with known mathematical results."""
        # f=0.5, p=2 → S_p = 1 / (0.5 + 0.5/2) = 1 / 0.75 = 1.333...
        result = calculate_speedup(0.5, 2)
        assert abs(result - 1.3333333333) < 1e-6

        # f=0.1, p=10 → S_p = 1 / (0.1 + 0.9/10) = 1 / 0.19 = 5.263...
        result = calculate_speedup(0.1, 10)
        expected = 1.0 / (0.1 + 0.9 / 10)
        assert abs(result - expected) < 1e-6

    def test_speedup_single_processor(self):
        """Test that speedup with 1 processor is always 1.0."""
        result = calculate_speedup(0.5, 1)
        assert result == 1.0

        result = calculate_speedup(0.1, 1)
        assert result == 1.0

    def test_speedup_fully_sequential(self):
        """Test that fully sequential program (f=1) has speedup of 1.0."""
        result = calculate_speedup(1.0, 10)
        assert result == 1.0

        result = calculate_speedup(1.0, 100)
        assert result == 1.0

    def test_speedup_fully_parallel(self):
        """Test that fully parallel program (f=0) achieves maximum speedup."""
        # f=0, p=4 → S_p = 1 / (0 + 1/4) = 4
        result = calculate_speedup(0.0, 4)
        assert abs(result - 4.0) < 1e-10

        result = calculate_speedup(0.0, 10)
        assert abs(result - 10.0) < 1e-10

    def test_speedup_invalid_fraction_low(self):
        """Test that negative fraction raises ValueError."""
        with pytest.raises(ValueError, match="Sequential fraction f must be in \\[0, 1\\]"):
            calculate_speedup(-0.1, 10)

    def test_speedup_invalid_fraction_high(self):
        """Test that fraction > 1 raises ValueError."""
        with pytest.raises(ValueError, match="Sequential fraction f must be in \\[0, 1\\]"):
            calculate_speedup(1.5, 10)

    def test_speedup_invalid_processors(self):
        """Test that processors < 1 raises ValueError."""
        with pytest.raises(ValueError, match="Number of processors p must be >= 1"):
            calculate_speedup(0.5, 0)

        with pytest.raises(ValueError, match="Number of processors p must be >= 1"):
            calculate_speedup(0.5, -1)


class TestCalculateEfficiency:
    """Test cases for calculate_efficiency function."""

    def test_efficiency_correctness(self):
        """Test that efficiency = speedup / p."""
        f, p = 0.5, 4
        efficiency = calculate_efficiency(f, p)
        speedup = calculate_speedup(f, p)
        expected = speedup / p
        assert abs(efficiency - expected) < 1e-10

    def test_efficiency_single_processor(self):
        """Test efficiency with single processor."""
        result = calculate_efficiency(0.5, 1)
        assert result == 1.0

    def test_efficiency_decreases_with_processors(self):
        """Test that efficiency decreases as processors increase."""
        f = 0.2
        eff1 = calculate_efficiency(f, 2)
        eff2 = calculate_efficiency(f, 10)
        assert eff1 > eff2

    def test_efficiency_fully_parallel(self):
        """Test efficiency for fully parallel program."""
        # f=0, efficiency should be 1.0 regardless of p
        result = calculate_efficiency(0.0, 10)
        assert abs(result - 1.0) < 1e-10


class TestCalculateExecutionTimeRatio:
    """Test cases for calculate_execution_time_ratio function."""

    def test_time_ratio_correctness(self):
        """Test that time_ratio = 1 / speedup."""
        f, p = 0.3, 5
        time_ratio = calculate_execution_time_ratio(f, p)
        speedup = calculate_speedup(f, p)
        expected = 1.0 / speedup
        assert abs(time_ratio - expected) < 1e-10

    def test_time_ratio_single_processor(self):
        """Test time ratio with single processor."""
        result = calculate_execution_time_ratio(0.5, 1)
        assert result == 1.0

    def test_time_ratio_decreases_with_speedup(self):
        """Test that time ratio decreases as speedup increases."""
        f = 0.1
        ratio1 = calculate_execution_time_ratio(f, 2)
        ratio2 = calculate_execution_time_ratio(f, 10)
        assert ratio1 > ratio2


class TestSimulateScaling:
    """Test cases for simulate_scaling function."""

    def test_simulate_scaling_returns_correct_structure(self):
        """Test that simulate_scaling returns correct dictionary structure."""
        results = simulate_scaling(0.5, 10)
        
        assert 'processors' in results
        assert 'speedups' in results
        assert 'efficiencies' in results
        assert 'time_ratios' in results

    def test_simulate_scaling_correct_array_sizes(self):
        """Test that all arrays have the correct size."""
        max_procs = 50
        results = simulate_scaling(0.5, max_procs)
        
        assert len(results['processors']) == max_procs
        assert len(results['speedups']) == max_procs
        assert len(results['efficiencies']) == max_procs
        assert len(results['time_ratios']) == max_procs

    def test_simulate_scaling_processor_range(self):
        """Test that processors array starts at 1 and ends at max_procs."""
        max_procs = 20
        results = simulate_scaling(0.5, max_procs)
        
        assert results['processors'][0] == 1
        assert results['processors'][-1] == max_procs

    def test_simulate_scaling_consistency(self):
        """Test that simulated results match individual calculations."""
        f = 0.2
        max_procs = 5
        results = simulate_scaling(f, max_procs)
        
        # Check that first processor (p=1) gives speedup = 1.0
        assert abs(results['speedups'][0] - 1.0) < 1e-10
        
        # Check a few individual values
        for i, p in enumerate(results['processors']):
            expected_speedup = calculate_speedup(f, p)
            assert abs(results['speedups'][i] - expected_speedup) < 1e-10
            
            expected_efficiency = calculate_efficiency(f, p)
            assert abs(results['efficiencies'][i] - expected_efficiency) < 1e-10
            
            expected_time_ratio = calculate_execution_time_ratio(f, p)
            assert abs(results['time_ratios'][i] - expected_time_ratio) < 1e-10

    def test_simulate_scaling_fully_sequential(self):
        """Test simulation with fully sequential program."""
        results = simulate_scaling(1.0, 10)
        
        # All speedups should be 1.0
        assert np.allclose(results['speedups'], 1.0)
        
        # Efficiencies should be 1/p
        for i, p in enumerate(results['processors']):
            assert abs(results['efficiencies'][i] - 1.0 / p) < 1e-10

    def test_simulate_scaling_invalid_fraction(self):
        """Test that invalid fraction raises ValueError."""
        with pytest.raises(ValueError):
            simulate_scaling(-0.1, 10)
        
        with pytest.raises(ValueError):
            simulate_scaling(1.5, 10)

    def test_simulate_scaling_invalid_max_procs(self):
        """Test that invalid max_procs raises ValueError."""
        with pytest.raises(ValueError):
            simulate_scaling(0.5, 0)
        
        with pytest.raises(ValueError):
            simulate_scaling(0.5, -1)

    def test_simulate_scaling_large_range(self):
        """Test simulation with large processor count for performance."""
        max_procs = 1000
        results = simulate_scaling(0.05, max_procs)
        
        assert len(results['processors']) == max_procs
        # Verify speedup increases but efficiency decreases
        assert results['speedups'][-1] > results['speedups'][0]
        assert results['efficiencies'][-1] < results['efficiencies'][0]

