"""
Levelized Return on Mobility Asset (LROMA) Calculator
Computes profitability metrics for mobility assets
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class LROMACalculator:
    def __init__(self, parameters: Optional[Dict] = None):
        self.parameters = parameters or {}
        
    def calculate_npv(self, cash_flows: List[float], discount_rate: float) -> float:
        """Calculate Net Present Value of cash flows"""
        return sum(cf / (1 + discount_rate) ** t 
                  for t, cf in enumerate(cash_flows, 1))
    
    def calculate_lroma(self, vehicle_params: Dict) -> float:
        """Calculate LROMA for a vehicle type"""
        # Extract parameters
        capex = vehicle_params['capex']
        annual_distance = vehicle_params['annual_distance']
        tco_per_km = vehicle_params['tco_per_km']
        freight_rate = vehicle_params['freight_rate']
        discount_rate = vehicle_params['discount_rate']
        vehicle_life = vehicle_params['vehicle_life']
        
        # Calculate annual profit
        annual_profit = annual_distance * (freight_rate - tco_per_km)
        
        # FIX: Create cash flows with CAPEX as initial investment
        cash_flows = [-capex]  # Year 0: initial investment (negative)
        cash_flows.extend([annual_profit] * vehicle_life)  # Years 1-N: annual profits
        
        # Calculate NPV (starting from year 0)
        npv = sum(cf / (1 + discount_rate) ** t 
                 for t, cf in enumerate(cash_flows))
        
        # Calculate present value of freight distance (years 1 to N)
        pv_distance = sum(annual_distance / (1 + discount_rate) ** t 
                         for t in range(1, vehicle_life + 1))
        
        # Calculate LROMA
        lroma = npv / pv_distance if pv_distance != 0 else 0
        
        return lroma
    
    def sensitivity_analysis(self, base_params: Dict, 
                           parameter_ranges: Dict) -> pd.DataFrame:
        """Perform sensitivity analysis on key parameters"""
        results = []
        
        for param_name, values in parameter_ranges.items():
            for value in values:
                modified_params = base_params.copy()
                modified_params[param_name] = value
                try:
                    lroma = self.calculate_lroma(modified_params)
                    results.append({
                        'parameter': param_name,
                        'value': value,
                        'lroma': lroma
                    })
                except (KeyError, ZeroDivisionError) as e:
                    print(f"Warning: Could not calculate LROMA for {param_name}={value}: {e}")
        
        return pd.DataFrame(results)
    
    def calculate_breakeven(self, vehicle_params: Dict, target_lroma: float = 0) -> Dict:
        """Calculate breakeven points for key parameters"""
        base_lroma = self.calculate_lroma(vehicle_params)
        
        breakeven_points = {}
        
        # Breakeven freight rate
        if base_lroma < target_lroma:
            current_freight = vehicle_params['freight_rate']
            # Simple linear approximation for breakeven
            required_increase = (target_lroma - base_lroma) * 2  # Simplified
            breakeven_points['freight_rate'] = current_freight + required_increase
        
        return breakeven_points