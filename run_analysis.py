#!/usr/bin/env python3
"""
Main analysis runner for Investor State Framework
Run with: python run_analysis.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lroma_calculator import LROMACalculator

def main():
    print("🚀 Running Investor State Framework Analysis...")
    
    # Test parameters
    base_parameters = {
        'capex': 4800000,
        'annual_distance': 100000,
        'tco_per_km': 13.20,
        'freight_rate': 25.00,
        'discount_rate': 0.08,
        'vehicle_life': 8
    }
    
    # Test calculation
    calculator = LROMACalculator({})
    result = calculator.calculate_lroma(base_parameters)
    
    print(f"✅ LROMA calculation successful: ¥{result:.2f}/km")
    print("✅ Basic framework is working!")

if __name__ == "__main__":
    main()