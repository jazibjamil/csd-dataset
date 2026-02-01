#!/usr/bin/env python3
import pandas as pd

# Load the data
df = pd.read_excel("DUMMY DATA FOR PRECISION AREAS.xlsx", sheet_name='Sheet6')

print("=== DETAILED DATA ANALYSIS ===")

# Time series data analysis
monthly_cols = [col for col in df.columns if "'" in col]
print(f"\nMonthly data columns: {monthly_cols}")

# Check if monthly data has consistent patterns
print(f"\nMonthly data statistics:")
for col in monthly_cols[:6]:  # First 6 months to show pattern
    zero_count = (df[col] == 0).sum()
    non_zero_count = (df[col] > 0).sum()
    print(f"  {col}: {zero_count} zeros ({zero_count/len(df)*100:.1f}%), {non_zero_count} non-zeros")

# Geographic distribution
print(f"\nGeographic Distribution:")
print(f"Regions: {df['Region'].value_counts().to_dict()}")
print(f"\nProvinces: {df['Province'].value_counts().head(10).to_dict()}")

# Product hierarchy analysis
print(f"\nProduct Hierarchy:")
print(f"Manufacturers: {df['KEY MANU  & KINZA'].value_counts().to_dict()}")
print(f"CSD Types: {df['CSD & CSD +'].value_counts().to_dict()}")
print(f"Flavor Segments: {df['CSD Flavor Segment'].value_counts().to_dict()}")
print(f"Reg/Diet: {df['REG/DIET'].value_counts().to_dict()}")
print(f"Pack Types: {df['PACK TYPE'].value_counts().to_dict()}")

# Market analysis
print(f"\nMarket Analysis:")
print(f"Market range: {df['MARKET'].min()} to {df['MARKET'].max()}")
print(f"Unique market values: {df['MARKET'].nunique()}")

# Check for any data patterns or issues
print(f"\nData Pattern Analysis:")
print(f"Total records: {len(df):,}")
print(f"Unique ITEMs: {df['ITEM'].nunique():,}")
print(f"Unique Precision Areas: {df['Precision Area'].nunique()}")

# Check if there are any aggregation levels visible
print(f"\nPotential aggregation levels:")
print(f"Records with same Region+Province: {df.groupby(['Region', 'Province']).size().describe()}")

# Sample some specific combinations
print(f"\nSample data combinations:")
sample = df.sample(10)
for idx, row in sample.iterrows():
    jan_val = row['Jan\'24']
    print(f"  {row['Region']} | {row['Province']} | {row['Precision Area'][:20]}... | {row['BRAND']} | {row['PACK SIZE']} | Jan'24: {jan_val}")