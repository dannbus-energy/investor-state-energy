"""
Fiscal Multiplier of Industrial Policy (FMIP) Model
Computes public investment returns including fiscal avoidances
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class FMIPCalculator:
    def __init__(self, parameters: Dict):
        self.parameters = parameters
        
    def calculate_present_value(self, cash_flows: List[float], 
                              discount_rate: float) -> float:
        """Calculate present value of cash flows"""
        if not cash_flows:
            return 0.0
        return sum(cf / (1 + discount_rate) ** t 
                  for t, cf in enumerate(cash_flows, 1))
    
    def calculate_fmip(self, scenario: str = "base_case") -> Dict:
        """Calculate FMIP for a given scenario"""
        # Check if scenario exists
        if scenario not in self.parameters:
            raise KeyError(f"Scenario '{scenario}' not found in parameters. Available: {list(self.parameters.keys())}")
        
        scenario_params = self.parameters[scenario]
        
        # Calculate present values with error checking
        try:
            pv_public_investment = self.calculate_present_value(
                scenario_params['public_investment_cashflows'],
                scenario_params['social_discount_rate']
            )
            
            pv_tax_revenues = self.calculate_present_value(
                scenario_params['tax_revenue_cashflows'],
                scenario_params['social_discount_rate']
            )
            
            pv_fiscal_avoidance = self.calculate_present_value(
                scenario_params['fiscal_avoidance_cashflows'],
                scenario_params['social_discount_rate']
            )
        except KeyError as e:
            raise KeyError(f"Missing required parameter in scenario '{scenario}': {e}")
        
        # Calculate FMIP with zero-division protection
        if pv_public_investment == 0:
            fmip = float('inf') if (pv_tax_revenues + pv_fiscal_avoidance) > 0 else 0.0
        else:
            fmip = (pv_tax_revenues + pv_fiscal_avoidance) / pv_public_investment
        
        return {
            'fmip': fmip,
            'pv_public_investment': pv_public_investment,
            'pv_tax_revenues': pv_tax_revenues,
            'pv_fiscal_avoidance': pv_fiscal_avoidance,
            'total_fiscal_return': pv_tax_revenues + pv_fiscal_avoidance,
            'scenario': scenario
        }
    
    def scenario_comparison(self, scenarios: Optional[List[str]] = None) -> pd.DataFrame:
        """Compare FMIP across different scenarios"""
        if scenarios is None:
            scenarios = ['base_case', 'pessimistic', 'optimistic', 'ssb_disruption']
        
        results = []
        
        for scenario in scenarios:
            try:
                fmip_result = self.calculate_fmip(scenario)
                results.append({
                    'scenario': scenario,
                    'fmip': fmip_result['fmip'],
                    'public_investment': fmip_result['pv_public_investment'],
                    'tax_revenues': fmip_result['pv_tax_revenues'],
                    'fiscal_avoidance': fmip_result['pv_fiscal_avoidance'],
                    'total_fiscal_return': fmip_result['total_fiscal_return']
                })
            except (KeyError, ValueError) as e:
                print(f"Warning: Could not calculate FMIP for scenario '{scenario}': {e}")
                # Optionally, you could append a row with NaN values instead
        
        return pd.DataFrame(results)
    
    def sensitivity_analysis(self, base_scenario: str, 
                           parameter_variations: Dict[str, List[float]]) -> pd.DataFrame:
        """Perform sensitivity analysis on key fiscal parameters"""
        results = []
        base_params = self.parameters[base_scenario]
        
        for param_name, values in parameter_variations.items():
            for value in values:
                try:
                    # Create modified scenario
                    modified_params = base_params.copy()
                    
                    # Handle different parameter types
                    if param_name.endswith('_cashflows'):
                        # Scale cash flows by multiplier
                        modified_params[param_name] = [x * value for x in modified_params[param_name]]
                    else:
                        modified_params[param_name] = value
                    
                    # Calculate FMIP with modified parameters
                    temp_calculator = FMIPCalculator({f"temp_{param_name}_{value}": modified_params})
                    fmip_result = temp_calculator.calculate_fmip(f"temp_{param_name}_{value}")
                    
                    results.append({
                        'parameter': param_name,
                        'value': value,
                        'fmip': fmip_result['fmip'],
                        'scenario': base_scenario
                    })
                    
                except Exception as e:
                    print(f"Warning: Sensitivity analysis failed for {param_name}={value}: {e}")
        
        return pd.DataFrame(results)