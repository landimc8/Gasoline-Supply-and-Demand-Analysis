"""
Quick country & regional balance analysis
For trader market positioning
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from data_loader import load_gasoline_data

# Setup output dir
os.makedirs('./results/figures/combined_analysis', exist_ok=True)

print("=== COUNTRIES & REGIONS ANALYSIS ===")

# Load market data
demand, supply = load_gasoline_data()

if demand is not None and supply is not None:
    # Calculate supply-demand gaps
    balance = supply - demand
    country_avg = balance.mean(axis=1)
    
    # Get top 15 imbalanced markets
    sorted_countries = country_avg.sort_values()
    top_countries = sorted_countries.head(15)
    
    # Define trading regions
    regions = {
        'ARA Hub': ['Netherlands', 'Belgium', 'Germany'],
        'North West': ['United Kingdom', 'France'], 
        'Mediterranean': ['Spain', 'Italy', 'Greece'],
        'East Europe': ['Poland', 'Czech Republic', 'Hungary']
    }
    
    # Calculate regional totals
    regional_data = []
    for region_name, countries in regions.items():
        region_total = 0
        for country in countries:
            if country in country_avg.index:
                region_total += country_avg[country]
        regional_data.append([region_name, region_total])
    
    regional_df = pd.DataFrame(regional_data, columns=['Region', 'Balance'])
    regional_sorted = regional_df.set_index('Region')['Balance'].sort_values()
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Country balance chart
    colors1 = ['red' if x < 0 else 'green' for x in top_countries.values]
    bars1 = ax1.barh(top_countries.index, top_countries.values, color=colors1)
    
    # Add value labels
    for bar, value in zip(bars1, top_countries.values):
        ax1.text(bar.get_width() + (10 if value >= 0 else -20), 
                 bar.get_y() + bar.get_height()/2,
                 f'{value:+.0f}', 
                 ha='left' if value >= 0 else 'right',
                 va='center',
                 fontweight='bold')
    
    ax1.axvline(x=0, color='black', linewidth=2)
    ax1.set_title('Country Balance')
    ax1.set_xlabel('Balance (Thousand kl)')
    ax1.grid(axis='x', alpha=0.3)
    
    # Regional balance chart
    colors2 = ['red' if x < 0 else 'green' for x in regional_sorted.values]
    bars2 = ax2.barh(regional_sorted.index, regional_sorted.values, color=colors2)
    
    for bar, value in zip(bars2, regional_sorted.values):
        ax2.text(bar.get_width() + (10 if value >= 0 else -20), 
                 bar.get_y() + bar.get_height()/2,
                 f'{value:+.0f}', 
                 ha='left' if value >= 0 else 'right', 
                 va='center',
                 fontweight='bold')
    
    ax2.axvline(x=0, color='black', linewidth=2)
    ax2.set_title('Regional Balance')
    ax2.set_xlabel('Balance (Thousand kl)')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./results/figures/combined_analysis/countries_regions.png')
    plt.show()
    
    print("Chart saved: countries_regions.png")
    
else:
    print("No data loaded")
