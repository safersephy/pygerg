"""
Tests for the PyGERG package.
"""

import unittest
import pytest
from pygerg import sgerg, GERG88


class TestGERG88(unittest.TestCase):
    """Test cases for the GERG-88 implementation."""
    
    def test_basic_calculation(self):
        """Test that the basic calculation works with standard parameters."""
        x3 = 0.01   # % CO2
        hs = 37.0   # Calorific value (MJ/m^3)
        rm = 0.7443  # Relative density
        x5 = 0.00   # 0% H2
        p = 8.0     # bar
        tc = 15.0   # °C
        
        x2, z, d = sgerg(x3, hs, rm, x5, p, tc)
        
        # Check results against expected values
        self.assertAlmostEqual(x2, 0.0214, delta=0.001)
        self.assertAlmostEqual(z, 0.970283, delta=0.0001)
        self.assertAlmostEqual(d, 321.222528, delta=0.1)
    
    def test_input_validation(self):
        """Test that the function validates input parameters correctly."""
        x3 = 0.01   # % CO2
        hs = 37.0   # Calorific value (MJ/m^3)
        rm = 0.7443  # Relative density
        x5 = 0.00   # 0% H2
        p = 8.0     # bar
        tc = 15.0   # °C
        
        # Test pressure out of range
        with self.assertRaises(ValueError):
            sgerg(x3, hs, rm, x5, 150.0, tc)
        
        # Test temperature out of range
        with self.assertRaises(ValueError):
            sgerg(x3, hs, rm, x5, p, 70.0)
        
        # Test CO2 fraction out of range
        with self.assertRaises(ValueError):
            sgerg(0.35, hs, rm, x5, p, tc)
        
        # Test calorific value out of range
        with self.assertRaises(ValueError):
            sgerg(x3, 50.0, rm, x5, p, tc)
        
        # Test relative density out of range
        with self.assertRaises(ValueError):
            sgerg(x3, hs, 0.5, x5, p, tc)
        
        # Test H2 fraction out of range
        with self.assertRaises(ValueError):
            sgerg(x3, hs, rm, 0.15, p, tc)
    
    def test_direct_class_usage(self):
        """Test direct usage of the GERG88 class."""
        calculator = GERG88()
        
        x3 = 0.01   # % CO2
        hs = 37.0   # Calorific value (MJ/m^3)
        rm = 0.7443  # Relative density
        x5 = 0.00   # 0% H2
        p = 8.0     # bar
        tc = 15.0   # °C
        
        x2, z, d = calculator.sgerg(x3, hs, rm, x5, p, tc)
        
        # Check results against expected values
        self.assertAlmostEqual(x2, 0.0214, delta=0.001)
        self.assertAlmostEqual(z, 0.970283, delta=0.0001)
        self.assertAlmostEqual(d, 321.222528, delta=0.1)


# Create parametrized tests for different gas compositions
@pytest.mark.parametrize("x3,hs,rm,x5,p,tc,expected_x2,expected_z,expected_d", [
    # Natural gas with different CO2 contents
    (0.00, 37.0, 0.7443, 0.00, 8.0, 15.0, 0.0214, 0.970283, 321.222528),
    (0.02, 37.0, 0.7443, 0.00, 8.0, 15.0, 0.0214, 0.970283, 321.222528),
    (0.05, 37.0, 0.7443, 0.00, 8.0, 15.0, 0.0214, 0.970283, 321.222528),
    
    # Varying pressure
    (0.01, 37.0, 0.7443, 0.00, 10.0, 15.0, 0.0214, 0.963, 405.6),
    (0.01, 37.0, 0.7443, 0.00, 20.0, 15.0, 0.0214, 0.928, 841.6),
    
    # Varying temperature
    (0.01, 37.0, 0.7443, 0.00, 8.0, 0.0, 0.0214, 0.968, 343.8),
    (0.01, 37.0, 0.7443, 0.00, 8.0, 30.0, 0.0214, 0.973, 301.3),
])
def test_parametrized(x3, hs, rm, x5, p, tc, expected_x2, expected_z, expected_d):
    """Parametrized test for different gas compositions and conditions."""
    x2, z, d = sgerg(x3, hs, rm, x5, p, tc)
    
    # Allow for some numerical differences
    assert abs(x2 - expected_x2) < 0.001
    assert abs(z - expected_z) < 0.01
    assert abs(d - expected_d) < 1.0


if __name__ == "__main__":
    unittest.main()