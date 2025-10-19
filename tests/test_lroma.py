import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from lroma_calculator import LROMACalculator

def test_lroma_basic():
    """Test basic LROMA calculation"""
    params = {
        'capex': 4800000,
        'annual_distance': 100000,
        'tco_per_km': 13.20,
        'freight_rate': 25.00,
        'discount_rate': 0.08,
        'vehicle_life': 8
    }
    
    calculator = LROMACalculator({})
    result = calculator.calculate_lroma(params)
    
    assert isinstance(result, float), "LROMA should return float"
    assert result > 0, "LROMA should be positive in base case"
    print("✅ LROMA basic test passed!")

if __name__ == "__main__":
    test_lroma_basic()