import pandas as pd
import matplotlib.pyplot as plt
import os
from data_loader import load_gasoline_data

# make output folder
os.makedirs('./results/figures/volatility_analysis', exist_ok=True)

print("Demand vs Supply Volatility")

# get the data
demand, supply = load_gasoline_data()

if demand is not None and supply is not None:
    # calc volatility (std/mean)
    demand_vol = demand.std(axis=1) / demand.mean(axis=1)
    top_demand_vol = demand_vol.sort_values(ascending=False).head(15)
    
    supply_vol = supply.std(axis=1) / supply.mean(axis=1)  
    top_supply_vol = supply_vol.sort_values(ascending=False).head(15)
    
    # create side-by-side chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # demand volatility chart
    bars1 = ax1.barh(top_demand_vol.index, top_demand_vol.values, color='orange', alpha=0.7)
    for bar, val in zip(bars1, top_demand_vol.values):
        ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontweight='bold')
    ax1.set_title('Demand Volatility - Top 15')
    ax1.set_xlabel('Coefficient of Variation')
    ax1.grid(axis='x', alpha=0.3)
    
    # supply volatility chart
    bars2 = ax2.barh(top_supply_vol.index, top_supply_vol.values, color='purple', alpha=0.7)
    for bar, val in zip(bars2, top_supply_vol.values):
        ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontweight='bold')
    ax2.set_title('Supply Volatility - Top 15')
    ax2.set_xlabel('Coefficient of Variation')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./results/figures/volatility_analysis/demand_supply_volatility.png')
    plt.show()
    
    # compare overall volatility
    avg_d_vol = demand_vol.mean()
    avg_s_vol = supply_vol.mean()
    
    print(f"Avg demand volatility: {avg_d_vol:.3f}")
    print(f"Avg supply volatility: {avg_s_vol:.3f}")
    
    if avg_d_vol > avg_s_vol:
        print("Demand more volatile overall")
    else:
        print("Supply more volatile overall")
    
    print("\nTop volatile demand markets:")
    print(top_demand_vol.head())
    
    print("\nTop volatile supply markets:")
    print(top_supply_vol.head())
    
    print("Chart saved")
    
else:
    print("No data loaded")
