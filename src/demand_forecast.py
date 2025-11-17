import statsmodels
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os
from data_loader import load_gasoline_data

def make_dirs():
    """Create output folders"""
    os.makedirs('./results/forecasts/demand', exist_ok=True)
    os.makedirs('./results/figures/forecasts', exist_ok=True)


def forecast_demand(demand_data, months=12):
    """Forecast demand for top countries"""
    forecasts = {}
    
    # Top countries by demand
    top_countries = demand_data.mean(axis=1).nlargest(6).index
    
    for country in top_countries:
        try:
            # Try exponential smoothing first
            model = ExponentialSmoothing(
                demand_data.loc[country],
                trend='add',
                seasonal='add',
                seasonal_periods=12
            )
            fitted = model.fit()
            forecast = fitted.forecast(months)
            forecasts[country] = forecast
        except:
            # Fallback to linear trend
            x = range(len(demand_data.loc[country]))
            y = demand_data.loc[country]
            trend = np.polyfit(x, y, 1)
            last_val = y.iloc[-1]
            forecast = [last_val + trend[0] * (i+1) for i in range(months)]
            forecasts[country] = pd.Series(forecast)
    
    return forecasts

def plot_forecasts(demand_data, forecasts, months=12):
    """Plot historical and forecast data"""
    plt.figure(figsize=(12, 8))
    
    # Future dates for x-axis
    last_date = pd.to_datetime(demand_data.columns[-1])
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=months,
        freq='MS'
    )
    
    # Plot each country
    for country, forecast in forecasts.items():
        # Historical
        hist = demand_data.loc[country]
        plt.plot(pd.to_datetime(hist.index), hist.values, 
                label=f'{country} - Hist', linewidth=2, alpha=0.7)
        
        # Forecast
        plt.plot(future_dates, forecast.values, 
                label=f'{country} - Forecast', linewidth=2, linestyle='--')
    
    plt.title('Demand Forecast - Top 6 Countries')
    plt.xlabel('Date')
    plt.ylabel('Demand (Thousand kl)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('./results/figures/forecasts/demand_forecast.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

def save_results(forecasts):
    """Save forecast data"""
    df = pd.DataFrame(forecasts)
    
    # Add dates
    future_dates = pd.date_range(start='2025-08-01', periods=len(df), freq='MS')
    df.index = future_dates
    
    df.to_csv('./results/forecasts/demand/demand_forecasts.csv')
    return df


def main():
    """Run the demand forecasting"""
    print("Running demand forecast...")
    
    make_dirs()
    
    demand, _ = load_gasoline_data()
    
    if demand is None:
        print("No demand data")
        return
    
    # Generate forecasts
    forecasts = forecast_demand(demand, 12)
    
    # Create plot
    plot_forecasts(demand, forecasts)
    
    # Save data
    forecast_df = save_results(forecasts)
    
    # Show summary
    print("\nDemand Forecast Summary:")
    for country in list(forecasts.keys())[:3]:
        current = demand.loc[country].iloc[-1]
        forecast_avg = forecasts[country].mean()
        change = ((forecast_avg - current) / current) * 100
        
        print(f"{country}:")
        print(f"  Current: {current:,.0f}")
        print(f"  Forecast: {forecast_avg:,.0f}")
        print(f"  Change: {change:+.1f}%")
    
    print("\nFiles saved in results/forecasts/demand/")

if __name__ == "__main__":
    main()
