import pandas as pd
import matplotlib.pyplot as plt
import os
from data_loader import load_gasoline_data

# make output folder
os.makedirs('./results/figures/yearly_analysis', exist_ok=True)

print("Yearly market trends")

# load data
demand, supply = load_gasoline_data()

if demand is not None and supply is not None:
    # fix date formatting
    demand.columns = pd.to_datetime(demand.columns)
    supply.columns = pd.to_datetime(supply.columns)
    
    # yearly totals
    y_demand = demand.sum(axis=0).resample('Y').sum()
    y_supply = supply.sum(axis=0).resample('Y').sum()
    balance = y_supply - y_demand
    
    years = y_demand.index.year
    
    # chart 1 - main trends
    plt.figure(figsize=(12, 8))
    
    plt.plot(years, y_demand.values, marker='o', linewidth=2, 
             label='Demand', color='blue', markersize=6)
    plt.plot(years, y_supply.values, marker='s', linewidth=2, 
             label='Supply', color='red', markersize=6)
    
    plt.title('European Gasoline Trends')
    plt.xlabel('Year')
    plt.ylabel('Volume (Thousand kl)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.savefig('./results/figures/yearly_analysis/yearly_trends.png')
    plt.show()
    
    # chart 2 - balance
    plt.figure(figsize=(10, 6))
    bar_colors = ['green' if x > 0 else 'red' for x in balance.values]
    bars = plt.bar(years, balance.values, color=bar_colors, alpha=0.7)
    
    # add value labels
    for bar, val in zip(bars, balance.values):
        offset = 1000 if val >= 0 else -3000
        plt.text(bar.get_x() + bar.get_width()/2, 
                bar.get_height() + offset,
                f'{val:+,.0f}', 
                ha='center', 
                va='bottom' if val >= 0 else 'top',
                fontweight='bold',
                fontsize=9)
    
    plt.axhline(y=0, color='black', linewidth=1)
    plt.title('Yearly Balance')
    plt.xlabel('Year')
    plt.ylabel('Supply - Demand')
    plt.xticks(years, rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('./results/figures/yearly_analysis/yearly_balance.png')
    plt.show()
    
    # chart 3 - growth
    d_growth = y_demand.pct_change() * 100
    s_growth = y_supply.pct_change() * 100
    
    plt.figure(figsize=(10, 6))
    growth_years = years[1:]
    plt.plot(growth_years, d_growth.values[1:], marker='o', 
             label='Demand', linewidth=2, color='darkblue', markersize=5)
    plt.plot(growth_years, s_growth.values[1:], marker='s', 
             label='Supply', linewidth=2, color='darkred', markersize=5)
    
    plt.axhline(y=0, color='black', linewidth=1, linestyle='--')
    plt.title('Growth Rates')
    plt.xlabel('Year')
    plt.ylabel('Change %')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(growth_years, rotation=45)
    plt.tight_layout()
    plt.savefig('./results/figures/yearly_analysis/growth_rates.png')
    plt.show()
    
    # output results
    current_yr = years[-1]
    d_current = y_demand.iloc[-1]
    s_current = y_supply.iloc[-1]
    b_current = balance.iloc[-1]
    
    print(f"{current_yr} results:")
    print(f"  Demand: {d_current:,.0f}")
    print(f"  Supply: {s_current:,.0f}")
    print(f"  Net: {b_current:+,.0f}")
    
    # growth numbers if available
    if len(y_demand) > 1:
        d_change = d_growth.iloc[-1]
        s_change = s_growth.iloc[-1]
        
        print(f"YoY change:")
        print(f"  Demand: {d_change:+.1f}%")
        print(f"  Supply: {s_change:+.1f}%")
    
    # market status
    if b_current > 0:
        print("Market balance: surplus")
    else:
        print("Market balance: deficit")
    
    print(f"Period: {years[0]}-{years[-1]}")
    print("Charts saved")
    
else:
    print("Data load failed")
