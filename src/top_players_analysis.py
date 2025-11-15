import pandas as pd
import matplotlib.pyplot as plt
import os
from data_loader import load_gasoline_data

# setup output folders
os.makedirs('./results/figures/top_players', exist_ok=True)

print("Top Markets Analysis 2016-2025")

# get the data
demand, supply = load_gasoline_data()

if demand is not None and supply is not None:
    # convert to datetime for proper handling
    demand.columns = pd.to_datetime(demand.columns)
    supply.columns = pd.to_datetime(supply.columns)
    
    # yearly averages
    yearly_demand = demand.resample('Y', axis=1).mean()
    yearly_supply = supply.resample('Y', axis=1).mean()
    
    # overall averages across all years
    avg_demand = demand.mean(axis=1)
    avg_supply = supply.mean(axis=1)
    
    # top 10 markets
    top_buyers = avg_demand.nlargest(10)
    top_sellers = avg_supply.nlargest(10)
    
    # create the main chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # buyers chart
    bars1 = ax1.barh(top_buyers.index, top_buyers.values, color='blue', alpha=0.7)
    for bar, val in zip(bars1, top_buyers.values):
        ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}', va='center', fontweight='bold')
    ax1.set_title('Top 10 Consumers (2016-2025 avg)')
    ax1.set_xlabel('Monthly Demand (Thousand kl)')
    ax1.grid(axis='x', alpha=0.3)
    
    # sellers chart
    bars2 = ax2.barh(top_sellers.index, top_sellers.values, color='green', alpha=0.7)
    for bar, val in zip(bars2, top_sellers.values):
        ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{val:.0f}', va='center', fontweight='bold')
    ax2.set_title('Top 10 Producers (2016-2025 avg)')
    ax2.set_xlabel('Monthly Supply (Thousand kl)')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./results/figures/top_players/top_markets_overall.png')
    plt.show()
    
    # market concentration
    total_demand = avg_demand.sum()
    total_supply = avg_supply.sum()
    
    top10_demand_pct = top_buyers.sum() / total_demand * 100
    top10_supply_pct = top_sellers.sum() / total_supply * 100
    
    print(f"Market share analysis:")
    print(f"  Top 10 consumers control {top10_demand_pct:.1f}% of demand")
    print(f"  Top 10 producers control {top10_supply_pct:.1f}% of supply")
    
    # net positions (exporters vs importers)
    net_flow = avg_supply - avg_demand
    big_exporters = net_flow[net_flow > 0].nlargest(5)
    big_importers = net_flow[net_flow < 0].nsmallest(5)
    
    print(f"\nMajor net exporters:")
    for market, surplus in big_exporters.items():
        print(f"  {market}: +{surplus:.0f}")
    
    print(f"\nMajor net importers:")
    for market, deficit in big_importers.items():
        print(f"  {market}: {deficit:.0f}")
    
    # market leaders
    top_consumer = top_buyers.index[0]
    top_producer = top_sellers.index[0]
    
    print(f"\nMarket leaders:")
    print(f"  Largest consumer: {top_consumer} ({top_buyers.iloc[0]:.0f})")
    print(f"  Largest producer: {top_producer} ({top_sellers.iloc[0]:.0f})")
    
    # save the summary data
    summary_data = pd.DataFrame({
        'avg_demand': avg_demand,
        'avg_supply': avg_supply,
        'net_position': net_flow
    })
    summary_data.to_csv('./results/tables/market_leaders_summary.csv')
    
    # check if leaders are consistent across years
    print(f"\nYearly leader check:")
    for year in yearly_demand.columns.year:
        yr_demand = yearly_demand[yearly_demand.columns[yearly_demand.columns.year == year]].iloc[:, 0]
        yr_supply = yearly_supply[yearly_supply.columns[yearly_supply.columns.year == year]].iloc[:, 0]
        
        top_yr_consumer = yr_demand.nlargest(1)
        top_yr_producer = yr_supply.nlargest(1)
        
        print(f"  {year}: {top_yr_consumer.index[0]} / {top_yr_producer.index[0]}")
    
    print("Analysis complete")
    
else:
    print("No data")
