#!/usr/bin/env python3
"""
Data Loader and Preprocessing Module
Saudi Arabian CSD Dataset Analysis Pipeline

This module handles loading, cleaning, and preparing the dataset for analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CSDDatasetLoader:
    """Comprehensive data loader for Saudi Arabian CSD dataset analysis."""
    
    def __init__(self, file_path="DUMMY DATA FOR PRECISION AREAS.xlsx", sheet_name='Sheet6'):
        """
        Initialize the dataset loader.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str): Name of the sheet to load
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.df_original = None
        self.df_long = None
        self.monthly_cols = []
        
    def load_data(self):
        """Load the original dataset from Excel file."""
        try:
            print("Loading dataset...")
            self.df_original = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            print(f"✅ Dataset loaded successfully: {self.df_original.shape[0]:,} rows × {self.df_original.shape[1]} columns")
            return True
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def identify_monthly_columns(self):
        """Identify and extract monthly sales columns."""
        self.monthly_cols = [col for col in self.df_original.columns if "'24" in col]
        print(f"✅ Found {len(self.monthly_cols)} monthly columns: {self.monthly_cols[:3]}...{self.monthly_cols[-3:]}")
        return self.monthly_cols
    
    def convert_to_long_format(self):
        """Convert data from wide to long format for time series analysis."""
        if self.df_original is None:
            print("❌ Please load data first")
            return False
            
        id_vars = ['Region', 'Province', 'Precision Area', 'MARKET', 'KEY MANU  & KINZA', 
                  'BRAND', 'Brand-2', 'CSD & CSD +', 'CSD Flavor Segment', 'REG/DIET', 
                  'KEY PACKS', 'SUB-BRAND', 'PACK TYPE', 'PACK SIZE', 'ITEM']
        
        try:
            print("Converting to long format...")
            self.df_long = pd.melt(self.df_original, 
                                  id_vars=id_vars,
                                  value_vars=self.monthly_cols,
                                  var_name='Month',
                                  value_name='Sales')
            
            # Clean and convert month names
            self.df_long['Month'] = self.df_long['Month'].str.replace("'", "")
            self.df_long['Date'] = pd.to_datetime(self.df_long['Month'], format='%b%y')
            self.df_long = self.df_long.sort_values('Date')
            
            # Add derived time columns
            self.df_long['Month_Name'] = self.df_long['Date'].dt.strftime('%B')
            self.df_long['Month_Num'] = self.df_long['Date'].dt.month
            self.df_long['Quarter'] = self.df_long['Date'].dt.quarter
            self.df_long['Year'] = self.df_long['Date'].dt.year
            
            print(f"✅ Long format created: {self.df_long.shape[0]:,} records")
            return True
            
        except Exception as e:
            print(f"❌ Error converting to long format: {e}")
            return False
    
    def clean_data(self):
        """Clean the dataset by handling missing values and duplicates."""
        if self.df_long is None:
            print("❌ Please convert to long format first")
            return False
            
        print("Cleaning dataset...")
        
        # Check for missing values
        missing_values = self.df_long.isnull().sum()
        if missing_values.sum() > 0:
            print(f"⚠️  Found missing values: {missing_values[missing_values > 0].to_dict()}")
        
        # Check for duplicates
        duplicates = self.df_long.duplicated().sum()
        if duplicates > 0:
            print(f"⚠️  Found {duplicates:,} duplicate records")
            self.df_long = self.df_long.drop_duplicates()
            print(f"✅ Removed duplicates, now {self.df_long.shape[0]:,} records")
        
        # Replace negative sales with 0 (data quality issue)
        negative_sales = (self.df_long['Sales'] < 0).sum()
        if negative_sales > 0:
            print(f"⚠️  Found {negative_sales:,} negative sales values, setting to 0")
            self.df_long.loc[self.df_long['Sales'] < 0, 'Sales'] = 0
        
        print("✅ Data cleaning completed")
        return True
    
    def create_derived_features(self):
        """Create derived features for enhanced analysis."""
        if self.df_long is None:
            print("❌ Please clean data first")
            return False
            
        print("Creating derived features...")
        
        # Sales in millions for easier analysis
        self.df_long['Sales_Millions'] = self.df_long['Sales'] / 1_000_000
        
        # Season indicators
        self.df_long['Season'] = self.df_long['Month_Num'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        # Ramadan impact (assuming October 2024 was Ramadan period)
        self.df_long['Ramadan_Period'] = self.df_long['Month_Num'].apply(lambda x: 1 if x == 10 else 0)
        
        # Pack size numeric extraction
        self.df_long['Pack_Size_Numeric'] = self.df_long['PACK SIZE'].str.extract('(\d+)').astype(float)
        
        # Market tier classification (based on market size)
        market_sizes = self.df_long.groupby('MARKET')['Sales'].sum().sort_values(ascending=False)
        market_tiers = pd.qcut(market_sizes, q=4, labels=['Tier 4', 'Tier 3', 'Tier 2', 'Tier 1'])
        self.df_long['Market_Tier'] = self.df_long['MARKET'].map(market_tiers)
        
        print("✅ Derived features created")
        return True
    
    def get_data_summary(self):
        """Generate comprehensive data summary."""
        if self.df_long is None:
            print("❌ No data available for summary")
            return None
            
        summary = {
            'total_records': len(self.df_long),
            'date_range': f"{self.df_long['Date'].min().strftime('%Y-%m-%d')} to {self.df_long['Date'].max().strftime('%Y-%m-%d')}",
            'regions': self.df_long['Region'].nunique(),
            'provinces': self.df_long['Province'].nunique(),
            'precision_areas': self.df_long['Precision Area'].nunique(),
            'markets': self.df_long['MARKET'].nunique(),
            'manufacturers': self.df_long['KEY MANU  & KINZA'].nunique(),
            'brands': self.df_long['BRAND'].nunique(),
            'items': self.df_long['ITEM'].nunique(),
            'total_sales': self.df_long['Sales'].sum(),
            'total_sales_millions': self.df_long['Sales'].sum() / 1_000_000,
            'zero_sales_records': (self.df_long['Sales'] == 0).sum(),
            'zero_sales_percentage': (self.df_long['Sales'] == 0).mean() * 100
        }
        
        return summary
    
    def save_processed_data(self, output_path="processed_csd_data.parquet"):
        """Save processed data for future use."""
        if self.df_long is None:
            print("❌ No processed data to save")
            return False
            
        try:
            self.df_long.to_parquet(output_path)
            print(f"✅ Processed data saved to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_processed_data(self, input_path="processed_csd_data.parquet"):
        """Load previously processed data."""
        try:
            self.df_long = pd.read_parquet(input_path)
            print(f"✅ Processed data loaded from {input_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading processed data: {e}")
            return False

def main():
    """Example usage of the dataset loader."""
    loader = CSDDatasetLoader()
    
    # Load and process data
    if loader.load_data():
        loader.identify_monthly_columns()
        loader.convert_to_long_format()
        loader.clean_data()
        loader.create_derived_features()
        
        # Display summary
        summary = loader.get_data_summary()
        if summary:
            print("\n" + "="*60)
            print("DATASET SUMMARY")
            print("="*60)
            for key, value in summary.items():
                if isinstance(value, float):
                    if 'percentage' in key:
                        print(f"{key.replace('_', ' ').title()}: {value:.1f}%")
                    elif 'millions' in key:
                        print(f"{key.replace('_', ' ').title()}: {value:.1f}M")
                    else:
                        print(f"{key.replace('_', ' ').title()}: {value:,.0f}")
                else:
                    print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Save processed data
        loader.save_processed_data()

if __name__ == "__main__":
    main()