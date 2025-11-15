# Demand-Supply Analysis for Gasoline-Project Proposal

## Project Category

Data Analysis \& Visualization

## Project Title

Demand-Supply Analysis for Gasoline

## Problem Statement

Much of the data available on gasoline flows is not comprehensive, and it is mostly cases dispersed across different websites. The data is also not consistently integrated into analytical models for easier analysis. Therefore, the purpose of the project is to analyse European gasoline supply and demand patterns using JODI data to identify market imbalances and trends that inform decisions, such as an increase in refining of the commodity or changes in prices.

## Planned Approach

**Single Commodity Focus**: European Gasoline

**Core Analysis Pipeline**:

1. **Data Ingestion**: Load and clean JODI gasoline data for key European regions
2. **Supply Analysis**: Refinery production, imports, exports, stock changes
3. **Demand Analysis**: Consumption patterns across countries and regions
4. **Balance Calculation**: Supply-demand gaps and inventory implications
5. **Correlation Analysis**
6. **Volatility Analysis**

**Technical Implementation**:

* Python data pipeline with pandas for ETL operations
* Automated data validation and cleaning procedures
* Interactive visualizations using matplotlib/seaborn
* Regional aggregation (ARA, MED, NWE) and country-level analysis

## Technologies \& Libraries

* Python 3.14
* pandas for data manipulation
* matplotlib \& seaborn for visualization
* numpy for numerical computations
* Jupyter Notebooks for exploratory analysis

## Data Sources

* Primary: JODI Oil World Database (Gasoline)
* Focus: European countries and regional aggregates

## Expected Challenges \& Solutions

* **Data Quality**: Handle missing values and reporting inconsistencies with robust validation
* **Regional Aggregation**: Standardize country groupings with clear methodology
* **Seasonal Adjustment**: Implement basic seasonal decomposition for trend analysis

## Success Criteria

* Clean, reproducible JODI dataset processing pipeline
* 5+ professional visualizations showing key market trends
* Supply-demand balance calculations for major regions
* Working Python code with clear documentation
* Identification of at least 3 significant market patterns

## Timeline

* **Week 1**: Data pipeline development \& initial cleaning
* **Week 2**: Supply-side analysis and visualization
* **Week 3**: Demand-side analysis and balance calculations
* **Week 4**: Final visualizations, documentation, and report

## Stretch Goals (If Time Permits)

* Basic seasonal decomposition of demand patterns
* Comparative analysis of regional differences
* Simple inventory build/draw analysis
