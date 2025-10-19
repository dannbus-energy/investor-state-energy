"""
Visualization module for Investor State framework
Generates all key figures from the paper
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
import warnings

class InvestorStateVisualizer:
    def __init__(self, style: str = "academic", figsize: Tuple[int, int] = (10, 8)):
        self.style = style
        self.figsize = figsize
        self.set_style()
        
    def set_style(self):
        """Set academic publication style with backward compatibility"""
        try:
            # Try modern seaborn style first
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            try:
                # Fallback to older seaborn
                plt.style.use('seaborn-whitegrid')
            except:
                # Final fallback to basic style
                plt.style.use('ggplot')
                warnings.warn("Using ggplot style as fallback. Install seaborn for better styling.")
        
        sns.set_palette("husl")
        
        # Set academic font parameters
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16
        })
        
    def plot_lroma_crossover(self, scenario_data: pd.DataFrame, 
                           save_path: Optional[str] = None) -> plt.Figure:
        """Create LROMA crossover map (Figure 2)"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Validate input data
        required_columns = ['bev_capex_reduction', 'charging_time_reduction', 'lroma_differential']
        missing_cols = [col for col in required_columns if col not in scenario_data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Create contour plot
        X = scenario_data['bev_capex_reduction']
        Y = scenario_data['charging_time_reduction'] 
        Z = scenario_data['lroma_differential']
        
        # Check if we have enough data points
        if len(X) < 10:
            warnings.warn(f"Low data points ({len(X)}) for contour plot. Results may be unreliable.")
        
        contour = ax.tricontourf(X, Y, Z, levels=20, cmap='RdBu_r', alpha=0.7)
        plt.colorbar(contour, ax=ax, label='LROMA Differential (FCEV - BEV) [¥/km]')
        
        # Add zero contour line
        try:
            zero_contour = ax.tricontour(X, Y, Z, levels=[0], colors='black', linewidths=2)
            # Label the zero contour
            ax.clabel(zero_contour, inline=True, fontsize=10, fmt='%1.1f')
        except Exception as e:
            warnings.warn(f"Could not draw zero contour: {e}")
        
        ax.set_xlabel('BEV CAPEX Reduction (%)')
        ax.set_ylabel('BEV Charging Time Reduction (%)')
        ax.set_title('LROMA Crossover Map: Technology Economics Under Evolution')
        
        # Add zones with background for better readability
        ax.text(0.15, 0.3, 'FCEV Superior', transform=ax.transAxes, 
                fontsize=12, fontweight='bold', color='darkred',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        ax.text(0.6, 0.8, 'BEV Superior', transform=ax.transAxes,
                fontsize=12, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            self._save_figure(fig, save_path)
            
        return fig
    
    def plot_fmip_composition(self, fmip_components: Dict, 
                            save_path: Optional[str] = None) -> plt.Figure:
        """Create FMIP composition chart (Figure 3)"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Validate input
        if 'tax_revenues' not in fmip_components or 'fiscal_avoidance' not in fmip_components:
            raise ValueError("fmip_components must contain 'tax_revenues' and 'fiscal_avoidance' keys")
        
        # Tax revenues breakdown
        tax_categories = list(fmip_components['tax_revenues'].keys())
        tax_values = list(fmip_components['tax_revenues'].values())
        
        bars1 = ax1.bar(tax_categories, tax_values, color=['#2E86AB', '#A23B72', '#F18F01'], alpha=0.8)
        ax1.set_title('Tax Revenues Composition (Billion JPY)')
        ax1.tick_params(axis='x', rotation=45)
        self._add_value_labels(ax1, bars1)
        
        # Fiscal avoidance breakdown
        avoidance_categories = list(fmip_components['fiscal_avoidance'].keys())
        avoidance_values = list(fmip_components['fiscal_avoidance'].values())
        
        bars2 = ax2.bar(avoidance_categories, avoidance_values, 
                       color=['#C73E1D', '#F4B393', '#6B8F71', '#2E86AB'], alpha=0.8)
        ax2.set_title('Fiscal Avoidance Composition (Billion JPY)')
        ax2.tick_params(axis='x', rotation=45)
        self._add_value_labels(ax2, bars2)
        
        # Add total values as text
        total_tax = sum(tax_values)
        total_avoidance = sum(avoidance_values)
        fig.suptitle(f'FMIP Components: Total Tax = ¥{total_tax:,.0f}B, Total Avoidance = ¥{total_avoidance:,.0f}B', 
                    fontsize=14, y=1.02)
        
        plt.tight_layout()
        
        if save_path:
            self._save_figure(fig, save_path)
            
        return fig
    
    def plot_fet_nexus(self, save_path: Optional[str] = None) -> plt.Figure:
        """Create FET Nexus systems diagram (Figure 4)"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create nodes
        nodes = {
            'Finance': (0, 1),
            'Energy': (1, 0), 
            'Transport': (0, -1)
        }
        
        node_colors = {'Finance': '#2E86AB', 'Energy': '#C73E1D', 'Transport': '#6B8F71'}
        
        # Draw nodes
        for node, (x, y) in nodes.items():
            ax.scatter(x, y, s=2000, alpha=0.7, edgecolors='black', linewidth=2,
                      color=node_colors[node])
            ax.text(x, y, node, ha='center', va='center', fontweight='bold', fontsize=12,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
        
        # Draw connections with labels
        connections = [
            ('Finance', 'Energy', 'De-risking\ninvestments'),
            ('Finance', 'Transport', 'LROMA\nguidance'),
            ('Energy', 'Finance', 'Price stability\n(CfD)'),
            ('Energy', 'Transport', 'Fuel cost'),
            ('Transport', 'Finance', 'FMIP\nreturns'),
            ('Transport', 'Energy', 'Hydrogen\ndemand')
        ]
        
        for start, end, label in connections:
            x1, y1 = nodes[start]
            x2, y2 = nodes[end]
            
            # Draw arrow with color based on direction
            color = node_colors[start]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color=color, alpha=0.7))
            
            # Add label with better positioning
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            # Offset labels slightly to avoid overlap
            offset_x, offset_y = 0.1, 0.1
            if 'Finance' in [start, end]:
                offset_y = -0.1 if 'Energy' in [start, end] else 0.1
            
            ax.text(mid_x + offset_x, mid_y + offset_y, label, ha='center', va='center', 
                   fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.9,
                                        edgecolor=color))
        
        ax.set_xlim(-1.2, 1.7)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title('Finance-Energy-Transport (FET) Nexus: Systems Integration', fontsize=14, pad=20)
        ax.axis('off')
        
        # Add a legend for node colors
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=node, alpha=0.7) 
                          for node, color in node_colors.items()]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.tight_layout()
        
        if save_path:
            self._save_figure(fig, save_path)
            
        return fig
    
    def _add_value_labels(self, ax, bars):
        """Add value labels on bars"""
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                   f'¥{height:,.0f}B',
                   ha='center', va='bottom', fontweight='bold')
    
    def _save_figure(self, fig: plt.Figure, save_path: str, dpi: int = 300, 
                    formats: list = ['png', 'pdf']):
        """Save figure in multiple formats"""
        for fmt in formats:
            if fmt == 'png':
                fig.savefig(save_path.replace('.png', '.png'), dpi=dpi, 
                           bbox_inches='tight', transparent=False)
            elif fmt == 'pdf':
                fig.savefig(save_path.replace('.png', '.pdf'), 
                           bbox_inches='tight', transparent=False)
            elif fmt == 'svg':
                fig.savefig(save_path.replace('.png', '.svg'), 
                           bbox_inches='tight', transparent=False)
    
    def create_summary_dashboard(self, lroma_data: pd.DataFrame, fmip_data: Dict,
                               save_path: Optional[str] = None) -> plt.Figure:
        """Create a comprehensive summary dashboard"""
        fig = plt.figure(figsize=(16, 12))
        
        # Create subplot grid
        gs = fig.add_gridspec(2, 2)
        
        # Plot 1: LROMA crossover
        ax1 = fig.add_subplot(gs[0, 0])
        # ... (implementation would go here)
        
        # Plot 2: FMIP composition
        ax2 = fig.add_subplot(gs[0, 1])
        # ... (implementation would go here)
        
        # Plot 3: FET Nexus
        ax3 = fig.add_subplot(gs[1, :])
        # ... (implementation would go here)
        
        fig.suptitle('Investor State Framework: Comprehensive Analysis Dashboard', 
                    fontsize=16, y=0.95)
        
        plt.tight_layout()
        
        if save_path:
            self._save_figure(fig, save_path)
            
        return fig