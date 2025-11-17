# European Gasoline Market Analysis

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Analysis](https://img.shields.io/badge/Analysis-Complete-green)
![Data Source](https://img.shields.io/badge/Data-JODI-brightgreen)
![Markets](https://img.shields.io/badge/Markets-25_European_Countries-orange)
![Forecasting](https://img.shields.io/badge/Forecasting-Time_Series-blueviolet)

# Demand-Supply Analysis for Gasoline

A data analysis project examining gasoline demand patterns in the European market.

## Project Structure
- `src/` - Python source code
- `data/` - Data files
- `notebooks/` - Jupyter notebooks

## Setup
```bash
pip install -r requirements.txt

**Abstract**
The oil market plays a crucial role in supporting global energy needs in sectors such as transportation and the generation of electricity. As such, it is important for businesses and governments to keep records to track the consumption of petroleum products for better planning in production to maintain a balance between demand and supply in order to avoid overproduction or shortage. However, it is challenging to find consolidated data or analyses that businesses and governments could directly use to make decisions, such as pricing. Thus, they need to conduct further analyses to identify trends that can be used to predict future consumption. This project, therefore, analyses one of the petroleum products, gasoline, using data from the Joint Organizations Data Initiative (JODI) website to investigate factors such as volatility, correction, trends, and future forecast of demand and supply of 25 countries in Europe, as well as three key regions: Amsterdam-Rotterdam-Antwerp (ARA), Mediterranean (MED), and Northwest Europe (NWE). To achieve this, the project implements a Python-based data analysis pipeline developed in Visual Studio Code and version-controlled using GitHub.
**Keywords**: Gasoline, supply, demand, European markets.
Features

- **Data Pipeline:** Automated data cleaning, validation, and processing from raw JODI Excel files.
- **Analysis** 
  - **Supply-Demand Balance:** Analysis of surplus and deficit markets.
  - **Correlation Analysis:** Measuring how closely supply tracks demand in each country.
  - **Volatility Profiling:** Evaluation of the most unstable markets using the Coefficient of Variation.
  - **Top Players:** Ranking of countries by highest consumption and production.
  - **Trend Analysis:** Analysis of the yearly changes, including the impact of COVID-19.
  - **Forecasting:** Projects demand and supply for key regions and countries into 2026.
- **Modular Architecture:** Clean, version-controlled code built in VSCode.

## 📈 Key Results & Visualizations

### 1. Supply-Demand Balance
![Supply-Demand Balance](https://github.com/landimc8/Gasoline-Supply-and-Demand-Analysis/blob/02af709284753949c82b6b559088be82c021cc8c/results/figures/combined_analysis/countries_regions.png)

*Italy and MED region show largest deficits, while NWE has consistent surplus*

### 2. Demand-Supply Correlation  
![Correlation Analysis](https://github.com/landimc8/Gasoline-Supply-and-Demand-Analysis/blob/02af709284753949c82b6b559088be82c021cc8c/results/figures/correlation/demand_supply_correlation.png)
*Austria and Turkey show near-perfect supply-demand tracking*

### 3. Market Volatility
![Volatility Analysis](https://github.com/landimc8/Gasoline-Supply-and-Demand-Analysis/blob/02af709284753949c82b6b559088be82c021cc8c/results/figures/volatility_analysis/demand_supply_volatility.png)
*Turkey (demand) and Norway (supply) exhibit highest volatility*

### 4. Demand Forecast
![Demand Forecast](https://github.com/landimc8/Gasoline-Supply-and-Demand-Analysis/blob/main/results/figures/volatility_analysis/demand_supply_volatility.png)
*2025 dip followed by 2026 recovery due to major events*


