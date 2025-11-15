import sys
import os

# fix import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_gasoline_data

def show_basic_stats():
    """Show basic gasoline market stats"""
    print("European Gasoline Analysis")
    print("==========================")
    
    # load data
    d, s = load_gasoline_data()
    
    if d is None:
        print("Couldn't load data")
        return
    
    # basic dataset info
    print(f"\nDataset: {len(d)} countries, {len(d.columns)} time periods")
    print(f"Date range: {d.columns[0]} to {d.columns[-1]}")
    
    # market totals
    total_demand = d.sum().sum()
    total_supply = s.sum().sum()
    balance = total_supply - total_demand
    
    print(f"\nMarket Totals:")
    print(f"Total demand: {total_demand:,.0f}")
    print(f"Total supply:  {total_supply:,.0f}")
    print(f"Net balance:   {balance:+,.0f}")
    
    # top markets
    avg_demand = d.mean(axis=1)
    top_markets = avg_demand.nlargest(3)
    
    print(f"\nTop 3 Markets:")
    for country, vol in top_markets.items():
        print(f"  {country}: {vol:,.0f}")
    
    # balance overview
    country_balance = s.mean(axis=1) - d.mean(axis=1)
    exporters = (country_balance > 0).sum()
    importers = (country_balance < 0).sum()
    
    print(f"\nMarket Balance:")
    print(f"Net exporters: {exporters}")
    print(f"Net importers: {importers}")

if __name__ == "__main__":
    show_basic_stats()