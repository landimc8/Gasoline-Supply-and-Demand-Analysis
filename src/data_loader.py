"""
.Module for loading and processing gasoline supply-demand data from Excel files.
"""
import openpyxl
import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict
import logging
import os
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_excel_file() -> Optional[str]:
    """
    Automatically find the Excel file in the project structure.
    """
    # Possible file names and locations
    possible_names = [
        "clean_gasoline_demand_supply_dataset_for_european_market.xlsx",
        "clean_gasoline_demand_supply_dataset_for_european_market.xls",
        "gasoline_data.xlsx",
        "gasoil_data.xlsx",
        "*.xlsx",  # Any Excel file
    ]
    
    possible_locations = [
        "./data",
        "../data", 
        ".",
        "..",
        "./data/raw",
        "../data/raw"
    ]
    
    for location in possible_locations:
        for name in possible_names:
            search_pattern = os.path.join(location, name)
            files = glob.glob(search_pattern)
            for file in files:
                if os.path.isfile(file) and os.path.getsize(file) > 0:
                    logger.info(f"Found Excel file: {file}")
                    return file
    
    logger.error("Could not find any Excel file")
    return None


def load_gasoline_data(file_path: str = None) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load gasoline supply and demand data from Excel file.
    """
    try:
        # If no file path provided, try to find it automatically
        if file_path is None:
            file_path = find_excel_file()
            if file_path is None:
                return None, None
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None, None
        
        logger.info(f"Loading data from: {file_path}")
        
        # First, let's see what sheets are available
        excel_file = pd.ExcelFile(file_path)
        logger.info(f"Available sheets: {excel_file.sheet_names}")
        
        # Try to find the correct sheet names
        demand_sheet = None
        supply_sheet = None
        
        for sheet in excel_file.sheet_names:
            if 'demand' in sheet.lower():
                demand_sheet = sheet
            if 'supply' in sheet.lower():
                supply_sheet = sheet
        
        # If we didn't find by name, use the first two sheets
        if demand_sheet is None and len(excel_file.sheet_names) >= 1:
            demand_sheet = excel_file.sheet_names[0]
        if supply_sheet is None and len(excel_file.sheet_names) >= 2:
            supply_sheet = excel_file.sheet_names[1]
            
        logger.info(f"Using demand sheet: {demand_sheet}")
        logger.info(f"Using supply sheet: {supply_sheet}")
        
        # Load demand data
        demand_df = pd.read_excel(
            file_path, 
            sheet_name=demand_sheet, 
            index_col=0
        )
        
        # Load supply data
        supply_df = pd.read_excel(
            file_path,
            sheet_name=supply_sheet,
            index_col=0
        )
        
        # Clean the data
        demand_df = clean_dataframe(demand_df, "Demand")
        supply_df = clean_dataframe(supply_df, "Supply")
        
        logger.info(f"✅ Successfully loaded demand data: {demand_df.shape}")
        logger.info(f"✅ Successfully loaded supply data: {supply_df.shape}")
        
        if not demand_df.empty:
            logger.info(f"Time range: {demand_df.columns[0]} to {demand_df.columns[-1]}")
            logger.info(f"Countries: {list(demand_df.index)}")
        
        return demand_df, supply_df
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None, None


def clean_dataframe(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    Clean the dataframe by handling missing values and formatting.
    """
    # Remove any completely empty rows and columns
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Convert column names to strings and clean them
    df.columns = df.columns.astype(str)
    
    # Fill missing values with 0
    df = df.fillna(0)
    
    logger.info(f"Cleaned {name} data: {df.shape}")
    return df


def validate_dataframes(demand_df: pd.DataFrame, supply_df: pd.DataFrame) -> Dict[str, bool]:
    """
    Validate the loaded gasoline data for consistency.
    """
    if demand_df is None or supply_df is None:
        logger.error("Cannot validate - dataframes are None")
        return {}
        
    validation_results = {}
    
    validation_results["demand_has_nulls"] = demand_df.isnull().any().any()
    validation_results["supply_has_nulls"] = supply_df.isnull().any().any()
    validation_results["demand_has_negatives"] = (demand_df < 0).any().any()
    validation_results["supply_has_negatives"] = (supply_df < 0).any().any()
    validation_results["indices_match"] = demand_df.index.equals(supply_df.index)
    validation_results["columns_match"] = demand_df.columns.equals(supply_df.columns)
    
    for check, result in validation_results.items():
        status = "PASS" if not result else "FAIL"
        logger.info(f"Validation {check}: {status}")
    
    return validation_results


def get_data_summary(demand_df: pd.DataFrame, supply_df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive summary of the gasoline dataset.
    """
    if demand_df is None or supply_df is None:
        return {}
        
    summary = {
        "n_countries": len(demand_df),
        "n_time_periods": len(demand_df.columns),
        "time_range": {
            "start": demand_df.columns[0],
            "end": demand_df.columns[-1]
        },
        "countries": list(demand_df.index),
        "demand_stats": {
            "total_volume": demand_df.sum().sum(),
            "average_per_country": demand_df.mean(axis=1).to_dict(),
            "top_5_countries": demand_df.mean(axis=1).nlargest(5).to_dict()
        },
        "supply_stats": {
            "total_volume": supply_df.sum().sum(),
            "average_per_country": supply_df.mean(axis=1).to_dict(),
            "top_5_countries": supply_df.mean(axis=1).nlargest(5).to_dict()
        }
    }
    
    return summary


if __name__ == "__main__":
    print("=== TESTING GASOLINE DATA LOADER ===\n")
    
    # First, let the function automatically find the file
    print("🔍 Searching for Excel file...")
    demand, supply = load_gasoline_data()
    
    if demand is not None and supply is not None:
        print("✅ Data loaded successfully!")
        print(f"\nDemand DataFrame:")
        print(f"Shape: {demand.shape}")
        print(f"Columns: {list(demand.columns)[:5]}...")  # First 5 columns
        print(f"Index (countries): {list(demand.index)}")
        print(f"\nSample of demand data:")
        print(demand.head())
        
        validation = validate_dataframes(demand, supply)
        print(f"\n✅ Data validation completed")
        
        summary = get_data_summary(demand, supply)
        print(f"✅ Data summary generated")
        print(f"   Countries: {summary['n_countries']}")
        print(f"   Time periods: {summary['n_time_periods']}")
        print(f"   Time range: {summary['time_range']['start']} to {summary['time_range']['end']}")
        
    else:
        print("❌ Failed to load data")
        print("\nPlease check:")
        print("1. The Excel file exists in your project")
        print("2. The file has .xlsx or .xls extension")
        print("3. You have pandas and openpyxl installed")
        print("\nRun this to see your files:")
        print("python diagnostic.py")
