import pandas as pd
import matplotlib.pyplot as plt
import os
from data_loader import load_gasoline_data

# Quick setup for output folders
os.makedirs('./results/figures/correlation', exist_ok=True)
os.makedirs('./results/tables', exist_ok=True)

def get_market_correlations(demand_data, supply_data):
    """Check how demand and supply move together for each market"""
    results = []
    
    for market in demand_data.index:
        if market in supply_data.index:
            # Calculate correlation for this market
            corr = demand_data.loc[market].corr(supply_data.loc[market])
            results.append({
                'market': market,
                'correlation': corr
            })
    
    return pd.DataFrame(results)

def plot_market_correlations(corr_data, top_markets=8):
    """Show which markets have strongest supply-demand relationships"""
    # Sort by correlation strength
    sorted_data = corr_data.sort_values('correlation', ascending=False)
    top_pos = sorted_data.head(top_markets)
    top_neg = sorted_data.tail(top_markets)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Markets where supply tracks demand well
    bars1 = ax1.barh(top_pos['market'], top_pos['correlation'], 
                    color='green', alpha=0.7)
    for bar, val in zip(bars1, top_pos['correlation']):
        ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center')
    ax1.set_title(f'Top {top_markets} - Supply Tracks Demand')
    ax1.set_xlabel('Correlation')
    ax1.set_xlim(0, 1)
    
    # Markets with inverse relationships
    bars2 = ax2.barh(top_neg['market'], top_neg['correlation'],
                    color='red', alpha=0.7)
    for bar, val in zip(bars2, top_neg['correlation']):
        ax2.text(bar.get_width() - 0.03, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center')
    ax2.set_title(f'Top {top_markets} - Inverse Relationship')
    ax2.set_xlabel('Correlation')
    ax2.set_xlim(-1, 0)
    
    plt.tight_layout()
    return fig

# Run the analysis
print("Checking market correlations...")

# Load the data
demand, supply = load_gasoline_data()

if demand is None or supply is None:
    print("No data - check files")
else:
    # Calculate all market correlations
    correlations = get_market_correlations(demand, supply)
    correlations = correlations.sort_values('correlation', ascending=False)
    
    # Create the chart
    fig = plot_market_correlations(correlations)
    plt.savefig('./results/figures/correlation/demand_supply_correlation.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Save the results
    correlations.to_csv('./results/tables/correlation_results.csv', index=False)
    
    # Print key insights
    avg_corr = correlations['correlation'].mean()
    print(f"Average market correlation: {avg_corr:.3f}")
    
    print("\nMarkets with strongest tracking:")
    for _, row in correlations.head(3).iterrows():
        print(f"  {row['market']}: {row['correlation']:.3f}")
    
    print("\nMarkets with weakest tracking:")
    for _, row in correlations.tail(3).iterrows():
        print(f"  {row['market']}: {row['correlation']:.3f}")
    
    # Quick market efficiency note
    if avg_corr > 0.7:
        print("\n✅ Markets generally efficient - supply follows demand")
    elif avg_corr > 0.4:
        print("\n⚠️  Mixed efficiency - some markets disconnected")
    else:
        print("\n❌ Low efficiency - supply/demand often move independently")
