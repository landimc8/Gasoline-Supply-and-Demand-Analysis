import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os
from data_loader import load_gasoline_data

def make_dirs():
    """Create output folders"""
    os.makedirs('./results/forecasts/supply', exist_ok=True)
    os.makedirs('./results/figures/forecasts', exist_ok=True)


def forecast_supply(supply_data, months=12):
    """Forecast supply for top countries"""
    forecasts = {}
    
    # Top countries by supply
    top_countries = supply_data.mean(axis=1).nlargest(6).index
    
    for country in top_countries:
        try:
            # Exponential smoothing
            model = ExponentialSmoothing(
                supply_data.loc[country],
                trend='add',
                seasonal='add',
                seasonal_periods=12
            )
            fitted = model.fit()
            forecast = fitted.forecast(months)
            forecasts[country] = forecast
        except:
            # Linear fallback
            x = range(len(supply_data.loc[country]))
            y = supply_data.loc[country]
            trend = np.polyfit(x, y, 1)
            last_val = y.iloc[-1]
            forecast = [last_val + trend[0] * (i+1) for i in range(months)]
            forecasts[country] = pd.Series(forecast)
    
    return forecasts

def plot_forecasts(supply_data, forecasts, months=12):
    """Plot historical and forecast data"""
    plt.figure(figsize=(12, 8))
    
    # Future dates
    last_date = pd.to_datetime(supply_data.columns[-1])
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=months,
        freq='MS'
    )
    
    # Plot each country
    for country, forecast in forecasts.items():
        # Historical
        hist = supply_data.loc[country]
        plt.plot(pd.to_datetime(hist.index), hist.values, 
                label=f'{country} - Hist', linewidth=2, alpha=0.7)
        
        # Forecast
        plt.plot(future_dates, forecast.values, 
                label=f'{country} - Forecast', linewidth=2, linestyle='--')
    
    plt.title('Supply Forecast - Top 6 Countries')
    plt.xlabel('Date')
    plt.ylabel('Supply (Thousand kl)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('./results/figures/forecasts/supply_forecast.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

def save_results(forecasts):
    """Save forecast data"""
    df = pd.DataFrame(forecasts)
    
    # Add dates
    future_dates = pd.date_range(start='2025-08-01', periods=len(df), freq='MS')
    df.index = future_dates
    
    df.to_csv('./results/forecasts/supply/supply_forecasts.csv')
    return df

def main():
    """Run the supply forecasting"""
    print("Running supply forecast...")
    
    make_dirs()
    
    _, supply = load_gasoline_data()
    
    if supply is None:
        print("No supply data")
        return
    
    # Generate forecasts
    forecasts = forecast_supply(supply, 12)
    
    # Create plot
    plot_forecasts(supply, forecasts)
    
    # Save data
    forecast_df = save_results(forecasts)
    
    # Show summary
    print("\nSupply Forecast Summary:")
    for country in list(forecasts.keys())[:3]:
        current = supply.loc[country].iloc[-1]
        forecast_avg = forecasts[country].mean()
        change = ((forecast_avg - current) / current) * 100
        
        print(f"{country}:")
        print(f"  Current: {current:,.0f}")
        print(f"  Forecast: {forecast_avg:,.0f}")
        print(f"  Change: {change:+.1f}%")
    
    print("\nFiles saved in results/forecasts/supply/")

if __name__ == "__main__":
    main()
