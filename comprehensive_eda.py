#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("=" * 80)
print("COMPREHENSIVE EXPLORATORY DATA ANALYSIS")
print("SAUDI ARABIAN CSD DATASET")
print("=" * 80)

# Load the data
file_path = "DUMMY DATA FOR PRECISION AREAS.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet6')

print(f"\nDataset Overview:")
print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Time Period: Jan 2024 - Dec 2024 (12 months)")
print(f"Geographic Coverage: {df['Region'].nunique()} regions, {df['Province'].nunique()} provinces, {df['Precision Area'].nunique()} precision areas")

# Prepare monthly columns for analysis
monthly_cols = [col for col in df.columns if "'24" in col]
print(f"Monthly sales data: {len(monthly_cols)} months")

# Convert data to long format for time series analysis
df_long = pd.melt(df, 
                  id_vars=['Region', 'Province', 'Precision Area', 'MARKET', 'KEY MANU  & KINZA', 
                          'BRAND', 'Brand-2', 'CSD & CSD +', 'CSD Flavor Segment', 'REG/DIET', 
                          'KEY PACKS', 'SUB-BRAND', 'PACK TYPE', 'PACK SIZE', 'ITEM'],
                  value_vars=monthly_cols,
                  var_name='Month',
                  value_name='Sales')

# Clean month names and convert to datetime
df_long['Month'] = df_long['Month'].str.replace("'", "")
df_long['Date'] = pd.to_datetime(df_long['Month'], format='%b%y')
df_long = df_long.sort_values('Date')

print(f"\nLong format dataset: {df_long.shape[0]:,} records")

# 1. TIME SERIES ANALYSIS
print("\n" + "=" * 60)
print("1. TIME SERIES ANALYSIS")
print("=" * 60)

# Overall monthly trends
monthly_total = df_long.groupby('Date')['Sales'].sum().reset_index()
monthly_total['Month_Name'] = monthly_total['Date'].dt.strftime('%B')
monthly_total['Sales_Millions'] = monthly_total['Sales'] / 1_000_000

# Add Month_Name to the main dataframe
df_long['Month_Name'] = df_long['Date'].dt.strftime('%B')

print("\nA. Overall Monthly Trends and Seasonality:")
print(monthly_total[['Month_Name', 'Sales_Millions']].round(2))

# Calculate seasonality metrics
peak_month = monthly_total.loc[monthly_total['Sales'].idxmax()]
low_month = monthly_total.loc[monthly_total['Sales'].idxmin()]
seasonality_ratio = peak_month['Sales'] / low_month['Sales']

print(f"\nSeasonality Analysis:")
print(f"Peak Month: {peak_month['Month_Name']} ({peak_month['Sales_Millions']:.2f}M)")
print(f"Lowest Month: {low_month['Month_Name']} ({low_month['Sales_Millions']:.2f}M)")
print(f"Seasonality Ratio: {seasonality_ratio:.2f}x")

# Monthly growth rates
monthly_total['Growth_Rate'] = monthly_total['Sales'].pct_change() * 100
avg_growth_rate = monthly_total['Growth_Rate'].mean()
print(f"Average Monthly Growth Rate: {avg_growth_rate:.2f}%")

# Sales volatility (coefficient of variation)
cv = monthly_total['Sales'].std() / monthly_total['Sales'].mean()
print(f"Sales Volatility (CV): {cv:.2f}")

# Year-over-year comparison (since we only have 2024, we'll compare H1 vs H2)
h1_total = monthly_total[monthly_total['Date'].dt.month <= 6]['Sales'].sum()
h2_total = monthly_total[monthly_total['Date'].dt.month > 6]['Sales'].sum()
h1_h2_growth = (h2_total - h1_total) / h1_total * 100

print(f"\nH1 vs H2 Comparison:")
print(f"H1 Total (Jan-Jun): {h1_total/1_000_000:.2f}M")
print(f"H2 Total (Jul-Dec): {h2_total/1_000_000:.2f}M")
print(f"H2 vs H1 Growth: {h1_h2_growth:.2f}%")

# 2. GEOGRAPHIC ANALYSIS
print("\n" + "=" * 60)
print("2. GEOGRAPHIC ANALYSIS")
print("=" * 60)

# Regional performance
regional_sales = df_long.groupby('Region')['Sales'].sum().sort_values(ascending=False)
regional_sales_millions = regional_sales / 1_000_000
total_sales = regional_sales.sum()

print("\nA. Regional Performance:")
for region, sales in regional_sales_millions.items():
    share = (sales / total_sales) * 100
    print(f"{region}: {sales:.2f}M ({share:.1f}% market share)")

# Province-level analysis
province_sales = df_long.groupby('Province')['Sales'].sum().sort_values(ascending=False)
province_sales_millions = province_sales / 1_000_000

print(f"\nB. Top 10 Provinces by Sales:")
for i, (province, sales) in enumerate(province_sales_millions.head(10).items(), 1):
    share = (sales / total_sales) * 100
    print(f"{i:2d}. {province}: {sales:.2f}M ({share:.1f}%)")

# Precision area hotspots
precision_sales = df_long.groupby('Precision Area')['Sales'].sum().sort_values(ascending=False)
precision_sales_millions = precision_sales / 1_000_000

print(f"\nC. Top 15 Precision Areas (Hotspots):")
for i, (area, sales) in enumerate(precision_sales_millions.head(15).items(), 1):
    share = (sales / total_sales) * 100
    print(f"{i:2d}. {area}: {sales:.2f}M ({share:.2f}%)")

# Geographic concentration metrics (Herfindahl-Hirschman Index)
regional_shares = regional_sales / total_sales
hhi_regional = (regional_shares ** 2).sum()
print(f"\nD. Geographic Concentration:")
print(f"Regional HHI: {hhi_regional:.4f} (0=perfect competition, 1=monopoly)")

# 3. PRODUCT PERFORMANCE ANALYSIS
print("\n" + "=" * 60)
print("3. PRODUCT PERFORMANCE ANALYSIS")
print("=" * 60)

# Manufacturer market share
manu_sales = df_long.groupby('KEY MANU  & KINZA')['Sales'].sum().sort_values(ascending=False)
manu_sales_millions = manu_sales / 1_000_000

print("\nA. Manufacturer Market Share:")
for manu, sales in manu_sales_millions.items():
    share = (sales / total_sales) * 100
    print(f"{manu}: {sales:.2f}M ({share:.1f}%)")

# Brand performance
brand_sales = df_long.groupby('BRAND')['Sales'].sum().sort_values(ascending=False)
brand_sales_millions = brand_sales / 1_000_000

print(f"\nB. Top 15 Brands by Sales:")
for i, (brand, sales) in enumerate(brand_sales_millions.head(15).items(), 1):
    share = (sales / total_sales) * 100
    print(f"{i:2d}. {brand}: {sales:.2f}M ({share:.1f}%)")

# Flavor segment analysis
flavor_sales = df_long.groupby('CSD Flavor Segment')['Sales'].sum().sort_values(ascending=False)
flavor_sales_millions = flavor_sales / 1_000_000

print(f"\nC. Flavor Segment Preferences:")
for flavor, sales in flavor_sales_millions.items():
    share = (sales / total_sales) * 100
    print(f"{flavor}: {sales:.2f}M ({share:.1f}%)")

# Pack type analysis
pack_type_sales = df_long.groupby('PACK TYPE')['Sales'].sum().sort_values(ascending=False)
pack_type_sales_millions = pack_type_sales / 1_000_000

print(f"\nD. Pack Type Performance:")
for pack_type, sales in pack_type_sales_millions.items():
    share = (sales / total_sales) * 100
    print(f"{pack_type}: {sales:.2f}M ({share:.1f}%)")

# Regular vs Diet
reg_diet_sales = df_long.groupby('REG/DIET')['Sales'].sum().sort_values(ascending=False)
reg_diet_sales_millions = reg_diet_sales / 1_000_000

print(f"\nE. Regular vs Diet Preferences:")
for reg_diet, sales in reg_diet_sales_millions.items():
    share = (sales / total_sales) * 100
    print(f"{reg_diet}: {sales:.2f}M ({share:.1f}%)")

# Pack size analysis (top 15)
pack_size_sales = df_long.groupby('PACK SIZE')['Sales'].sum().sort_values(ascending=False)
pack_size_sales_millions = pack_size_sales / 1_000_000

print(f"\nF. Top 15 Pack Sizes:")
for i, (size, sales) in enumerate(pack_size_sales_millions.head(15).items(), 1):
    share = (sales / total_sales) * 100
    print(f"{i:2d}. {size}: {sales:.2f}M ({share:.1f}%)")

# 4. CROSS-DIMENSIONAL ANALYSIS
print("\n" + "=" * 60)
print("4. CROSS-DIMENSIONAL ANALYSIS")
print("=" * 60)

# Seasonal patterns by region
print("\nA. Seasonal Patterns by Region (Top 5 Regions):")
top_regions = regional_sales.head(5).index.tolist()
for region in top_regions:
    region_data = df_long[df_long['Region'] == region].groupby('Month_Name')['Sales'].sum()
    peak_month_region = region_data.idxmax()
    total_region_sales = region_data.sum()
    peak_share = (region_data[peak_month_region] / total_region_sales) * 100
    print(f"{region}: Peak in {peak_month_region} ({peak_share:.1f}% of region's annual sales)")

# Flavor preferences by region
print(f"\nB. Top Flavor by Region:")
for region in top_regions:
    region_flavors = df_long[df_long['Region'] == region].groupby('CSD Flavor Segment')['Sales'].sum()
    top_flavor = region_flavors.idxmax()
    flavor_share = (region_flavors[top_flavor] / region_flavors.sum()) * 100
    print(f"{region}: {top_flavor} ({flavor_share:.1f}%)")

# Pack type trends over time (comparing Jan vs Dec)
jan_sales = df_long[df_long['Month'] == 'Jan24'].groupby('PACK TYPE')['Sales'].sum()
dec_sales = df_long[df_long['Month'] == 'Dec24'].groupby('PACK TYPE')['Sales'].sum()
pack_growth = pd.DataFrame({'Jan': jan_sales, 'Dec': dec_sales}).fillna(0)
pack_growth['Growth_%'] = ((pack_growth['Dec'] - pack_growth['Jan']) / pack_growth['Jan'] * 100).replace([np.inf, -np.inf], 0)

print(f"\nC. Pack Type Growth (Jan vs Dec):")
print(pack_growth['Growth_%'].sort_values(ascending=False).round(1))

# Market penetration by manufacturer in each region
print(f"\nD. Market Penetration (Manufacturer Share by Region) - Top 3 Regions:")
for region in top_regions[:3]:
    region_data = df_long[df_long['Region'] == region]
    region_total = region_data['Sales'].sum()
    manu_penetration = region_data.groupby('KEY MANU  & KINZA')['Sales'].sum() / region_total * 100
    top_manu = manu_penetration.idxmax()
    top_share = manu_penetration.max()
    print(f"{region}: {top_manu} leads with {top_share:.1f}% share")

# 5. STATISTICAL SUMMARY
print("\n" + "=" * 60)
print("5. STATISTICAL SUMMARY")
print("=" * 60)

# Descriptive statistics
print("\nA. Sales Descriptive Statistics:")
sales_stats = df_long['Sales'].describe()
print(f"Count: {sales_stats['count']:,.0f}")
print(f"Mean: {sales_stats['mean']:,.2f}")
print(f"Std Dev: {sales_stats['std']:,.2f}")
print(f"Min: {sales_stats['min']:,.2f}")
print(f"25%: {sales_stats['25%']:,.2f}")
print(f"Median: {sales_stats['50%']:,.2f}")
print(f"75%: {sales_stats['75%']:,.2f}")
print(f"Max: {sales_stats['max']:,.2f}")

# Distribution analysis
zero_sales = (df_long['Sales'] == 0).sum()
positive_sales = (df_long['Sales'] > 0).sum()
print(f"\nB. Distribution Analysis:")
print(f"Zero Sales Records: {zero_sales:,} ({zero_sales/len(df_long)*100:.1f}%)")
print(f"Positive Sales Records: {positive_sales:,} ({positive_sales/len(df_long)*100:.1f}%)")

# Skewness and kurtosis
from scipy import stats
skewness = stats.skew(df_long['Sales'])
kurtosis = stats.kurtosis(df_long['Sales'])
print(f"Sales Skewness: {skewness:.2f} (>{1} = highly skewed)")
print(f"Sales Kurtosis: {kurtosis:.2f} (>{3} = heavy-tailed)")

# Outlier detection (using IQR method)
Q1 = sales_stats['25%']
Q3 = sales_stats['75%']
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df_long[(df_long['Sales'] < lower_bound) | (df_long['Sales'] > upper_bound)]
print(f"\nC. Outlier Detection:")
print(f"IQR Boundaries: [{lower_bound:.2f}, {upper_bound:.2f}]")
print(f"Outliers: {len(outliers):,} records ({len(outliers)/len(df_long)*100:.1f}%)")

# Correlation analysis (monthly sales correlation)
monthly_pivot = df_long.pivot_table(values='Sales', index='Region', columns='Month', aggfunc='sum')
correlation_matrix = monthly_pivot.corr()
avg_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
print(f"\nD. Monthly Sales Correlation:")
print(f"Average Monthly Correlation: {avg_correlation:.3f}")

# Top correlations
correlations = []
for i in range(len(monthly_cols)):
    for j in range(i+1, len(monthly_cols)):
        corr_val = correlation_matrix.iloc[i, j]
        correlations.append((monthly_cols[i], monthly_cols[j], corr_val))

correlations.sort(key=lambda x: abs(x[2]), reverse=True)
print("Top 5 Monthly Correlations:")
for month1, month2, corr in correlations[:5]:
    print(f"  {month1} ↔ {month2}: {corr:.3f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - Key Insights Generated")
print("=" * 80)

# Generate insights summary
print("\nKEY BUSINESS INSIGHTS:")
print("1. Market concentration is " + ("HIGH" if hhi_regional > 0.25 else "MODERATE" if hhi_regional > 0.15 else "LOW"))
print(f"2. Seasonality factor: {seasonality_ratio:.1f}x between peak and low months")
print(f"3. Market volatility: {cv:.2f} (coefficient of variation)")
print(f"4. Top manufacturer commands {manu_sales_millions.max()/total_sales*100:.1f}% market share")
print(f"5. {reg_diet_sales_millions.idxmax()} products dominate with {reg_diet_sales_millions.max()/total_sales*100:.1f}% share")
print(f"6. {flavor_sales_millions.idxmax()} is the preferred flavor segment")