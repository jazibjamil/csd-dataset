#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')

print("=" * 80)
print("STRATEGIC BUSINESS INTELLIGENCE - HIDDEN PATTERNS & DEEP INSIGHTS")
print("SAUDI ARABIAN CSD DATASET")
print("=" * 80)

# Load and prepare data
file_path = "DUMMY DATA FOR PRECISION AREAS.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet6')

monthly_cols = [col for col in df.columns if "'24" in col]
df_long = pd.melt(df, 
                  id_vars=['Region', 'Province', 'Precision Area', 'MARKET', 'KEY MANU  & KINZA', 
                          'BRAND', 'Brand-2', 'CSD & CSD +', 'CSD Flavor Segment', 'REG/DIET', 
                          'KEY PACKS', 'SUB-BRAND', 'PACK TYPE', 'PACK SIZE', 'ITEM'],
                  value_vars=monthly_cols,
                  var_name='Month',
                  value_name='Sales')

df_long['Month'] = df_long['Month'].str.replace("'", "")
df_long['Date'] = pd.to_datetime(df_long['Month'], format='%b%y')
df_long = df_long.sort_values('Date')
df_long['Month_Name'] = df_long['Date'].dt.strftime('%B')
df_long['Month_Num'] = df_long['Date'].dt.month
df_long['Quarter'] = df_long['Date'].dt.quarter
total_sales = df_long['Sales'].sum()

# 1. HIDDEN MARKET PATTERNS
print("\n" + "=" * 60)
print("1. HIDDEN MARKET PATTERNS")
print("=" * 60)

# Unconventional correlations - weather patterns proxy
print("\nA. Temperature-Inferred Seasonal Patterns:")
monthly_sales = df_long.groupby('Month_Num')['Sales'].sum().reset_index()
# Assuming hotter months (Jun-Sep) show different patterns
hot_months = [6, 7, 8, 9]
cool_months = [11, 12, 1, 2, 3, 4]
hot_sales = monthly_sales[monthly_sales['Month_Num'].isin(hot_months)]['Sales'].sum()
cool_sales = monthly_sales[monthly_sales['Month_Num'].isin(cool_months)]['Sales'].sum()
print(f"Hot Season Sales: {hot_sales/1_000_000:.1f}M ({hot_sales/total_sales*100:.1f}%)")
print(f"Cool Season Sales: {cool_sales/1_000_000:.1f}M ({cool_sales/total_sales*100:.1f}%)")
print(f"Hot/Cool Ratio: {hot_sales/cool_sales:.2f}x")

# Market anomalies - zero sales patterns
print("\nB. Market Anomalies & Distribution Gaps:")
zero_analysis = df_long[df_long['Sales'] == 0].copy()
total_records = len(df_long)
print(f"Zero Sales Records: {len(zero_analysis):,} ({len(zero_analysis)/total_records*100:.1f}%)")

# Geographic concentration of zeros
zero_by_region = zero_analysis.groupby('Region').size()
total_by_region = df_long.groupby('Region').size()
zero_pct_by_region = (zero_by_region / total_by_region * 100).sort_values(ascending=False)
print("\nZero Sales % by Region (Top 5):")
for region, pct in zero_pct_by_region.head(5).items():
    print(f"  {region}: {pct:.1f}%")

# Manufacturer-specific zero patterns
zero_by_manu = zero_analysis.groupby('KEY MANU  & KINZA').size()
total_by_manu = df_long.groupby('KEY MANU  & KINZA').size()
zero_pct_by_manu = (zero_by_manu / total_by_manu * 100).sort_values(ascending=False)
print("\nZero Sales % by Manufacturer:")
for manu, pct in zero_pct_by_manu.items():
    print(f"  {manu}: {pct:.1f}%")

# Emerging trends - pack type evolution
print("\nC. Emerging Package Trends:")
pack_monthly = df_long.groupby(['Month_Num', 'PACK TYPE'])['Sales'].sum().reset_index()
pack_pivot = pack_monthly.pivot(index='Month_Num', columns='PACK TYPE', values='Sales').fillna(0)

# Calculate growth rates for each pack type
pack_growth = {}
for pack_type in pack_pivot.columns:
    if pack_pivot[pack_type].iloc[0] > 0:
        growth = (pack_pivot[pack_type].iloc[-1] - pack_pivot[pack_type].iloc[0]) / pack_pivot[pack_type].iloc[0] * 100
        pack_growth[pack_type] = growth

print("Package Type Growth (Jan vs Dec):")
for pack_type, growth in sorted(pack_growth.items(), key=lambda x: x[1], reverse=True):
    print(f"  {pack_type}: {growth:.1f}%")

# 2. STRATEGIC BUSINESS INTELLIGENCE
print("\n" + "=" * 60)
print("2. STRATEGIC BUSINESS INTELLIGENCE")
print("=" * 60)

# White space opportunities - underserved segments
print("\nA. White Space Opportunities:")

# Diet segment penetration by region
diet_by_region = df_long[df_long['REG/DIET'] == 'DIET'].groupby('Region')['Sales'].sum()
total_by_region = df_long.groupby('Region')['Sales'].sum()
diet_penetration = (diet_by_region / total_by_region * 100).fillna(0).sort_values()
print("\nDiet Segment Penetration by Region (Lowest = Opportunity):")
for region, penetration in diet_penetration.head(3).items():
    print(f"  {region}: {penetration:.1f}% diet penetration")

# Flavor segment gaps by region
flavor_region = df_long.groupby(['Region', 'CSD Flavor Segment'])['Sales'].sum().reset_index()
flavor_totals = flavor_region.groupby('Region')['Sales'].sum()
flavor_shares = []
for region in flavor_region['Region'].unique():
    region_data = flavor_region[flavor_region['Region'] == region].copy()
    region_total = flavor_totals[region]
    region_data['Share'] = region_data['Sales'] / region_total * 100
    flavor_shares.append(region_data)

# Find flavor gaps
print("\nFlavor Segment Gaps (Regions with <5% share for major flavors):")
major_flavors = ['COLA', 'CITRUS', 'MANGO', 'ORANGE']
for flavor in major_flavors:
    gaps = []
    for region in df_long['Region'].unique():
        flavor_sales = df_long[(df_long['Region'] == region) & 
                              (df_long['CSD Flavor Segment'] == flavor)]['Sales'].sum()
        region_total = df_long[df_long['Region'] == region]['Sales'].sum()
        share = (flavor_sales / region_total * 100) if region_total > 0 else 0
        if share < 5 and region_total > 0:
            gaps.append((region, share))
    if gaps:
        print(f"  {flavor}: {len(gaps)} regions with <5% penetration")

# Geographic expansion opportunities
print("\nB. Geographic Expansion Opportunities:")

# Province-level opportunity scoring
province_metrics = df_long.groupby('Province').agg({
    'Sales': 'sum',
    'Precision Area': 'nunique',
    'BRAND': 'nunique'
}).reset_index()

province_metrics['Sales_Per_Area'] = province_metrics['Sales'] / province_metrics['Precision Area']
province_metrics['Brand_Density'] = province_metrics['BRAND'] / province_metrics['Precision Area']

# Calculate opportunity score (inverse of current performance)
province_metrics['Opportunity_Score'] = (
    (province_metrics['Sales_Per_Area'].rank(ascending=True) * 0.4) +
    (province_metrics['Brand_Density'].rank(ascending=True) * 0.3) +
    (province_metrics['Sales'].rank(ascending=True) * 0.3)
)

top_opportunities = province_metrics.nlargest(5, 'Opportunity_Score')
print("\nTop 5 Provinces for Expansion:")
for _, row in top_opportunities.iterrows():
    print(f"  {row['Province']}: {row['Sales']/1_000_000:.1f}M sales, "
          f"{row['Precision Area']} areas, Score: {row['Opportunity_Score']:.1f}")

# Competitive vulnerabilities
print("\nC. Competitive Vulnerabilities:")

# Manufacturer concentration risk
manu_region = df_long.groupby(['Region', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
region_totals = manu_region.groupby('Region')['Sales'].sum()
vulnerabilities = []

for region in df_long['Region'].unique():
    region_manu = manu_region[manu_region['Region'] == region]
    region_total = region_totals[region]
    region_manu['Share'] = region_manu['Sales'] / region_total * 100
    
    # Check for high concentration (>70% for single manufacturer)
    top_share = region_manu['Share'].max()
    if top_share > 70:
        top_manu = region_manu.loc[region_manu['Share'].idxmax(), 'KEY MANU  & KINZA']
        vulnerabilities.append((region, top_manu, top_share))

print("\nHigh Concentration Risks (>70% market share):")
for region, manu, share in vulnerabilities:
    print(f"  {region}: {manu} dominates with {share:.1f}% share")

# 3. OPERATIONAL INSIGHTS
print("\n" + "=" * 60)
print("3. OPERATIONAL INSIGHTS")
print("=" * 60)

# Distribution inefficiencies
print("\nA. Distribution Inefficiencies:")

# Zero sales patterns by pack type
zero_by_pack = zero_analysis.groupby('PACK TYPE').size()
total_by_pack = df_long.groupby('PACK TYPE').size()
zero_pct_by_pack = (zero_by_pack / total_by_pack * 100).sort_values(ascending=False)
print("Zero Sales % by Pack Type (Inefficiency Indicator):")
for pack_type, pct in zero_pct_by_pack.items():
    print(f"  {pack_type}: {pct:.1f}%")

# Sales frequency analysis
sales_frequency = df_long[df_long['Sales'] > 0].copy()
frequency_by_product = sales_frequency.groupby(['BRAND', 'PACK SIZE']).size().reset_index(name='Months_Sold')
total_months = 12
frequency_by_product['Frequency_%'] = (frequency_by_product['Months_Sold'] / total_months * 100)

low_frequency_products = frequency_by_product[frequency_by_product['Frequency_%'] < 50]
print(f"\nLow Frequency Products (<50% months availability): {len(low_frequency_products)} SKUs")

# Inventory optimization opportunities
print("\nB. Inventory Optimization Opportunities:")

# Seasonal variance analysis
product_seasonality = df_long.groupby(['BRAND', 'PACK SIZE'])['Sales'].agg(['mean', 'std']).reset_index()
product_seasonality['CV'] = product_seasonality['std'] / product_seasonality['mean']
high_variance_products = product_seasonality[product_seasonality['CV'] > 1.0]
print(f"High Seasonality Products (CV > 1.0): {len(high_variance_products)} SKUs")

# Top high-variance products
high_variance_sorted = high_variance_products.sort_values('CV', ascending=False)
print("\nTop 5 Most Seasonal Products:")
for _, row in high_variance_sorted.head(5).iterrows():
    print(f"  {row['BRAND']} {row['PACK SIZE']}: CV = {row['CV']:.2f}")

# Product lifecycle insights
print("\nC. Product Lifecycle Insights:")

# Growth/decline analysis
monthly_products = df_long.groupby(['Month_Num', 'BRAND'])['Sales'].sum().reset_index()
product_growth = monthly_products.pivot(index='Month_Num', columns='BRAND', values='Sales').fillna(0)

growth_rates = {}
for brand in product_growth.columns:
    if product_growth[brand].iloc[0] > 0:
        growth = (product_growth[brand].iloc[-1] - product_growth[brand].iloc[0]) / product_growth[brand].iloc[0] * 100
        growth_rates[brand] = growth

print("Brand Growth Rates (Jan vs Dec):")
growing_brands = [(brand, rate) for brand, rate in growth_rates.items() if rate > 10]
declining_brands = [(brand, rate) for brand, rate in growth_rates.items() if rate < -10]

if growing_brands:
    print("\nGrowing Brands (>10% growth):")
    for brand, rate in sorted(growing_brands, key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {brand}: {rate:.1f}% growth")

if declining_brands:
    print("\nDeclining Brands (<-10% growth):")
    for brand, rate in sorted(declining_brands, key=lambda x: x[1])[:5]:
        print(f"  {brand}: {rate:.1f}% decline")

# 4. PREDICTIVE PATTERNS
print("\n" + "=" * 60)
print("4. PREDICTIVE PATTERNS")
print("=" * 60)

# Leading indicators for market changes
print("\nA. Leading Indicators:")

# Pack type as leading indicator
pack_sales = df_long.groupby(['Month_Num', 'PACK TYPE'])['Sales'].sum().reset_index()
total_monthly = df_long.groupby('Month_Num')['Sales'].sum()
pack_sales['Market_Share'] = pack_sales.apply(lambda x: x['Sales'] / total_monthly.loc[x['Month_Num']] * 100, axis=1)

# Identify emerging pack types (growing market share)
emerging_packs = []
for pack_type in pack_sales['PACK TYPE'].unique():
    pack_data = pack_sales[pack_sales['PACK TYPE'] == pack_type].sort_values('Month_Num')
    if len(pack_data) >= 3:
        recent_share = pack_data.tail(3)['Market_Share'].mean()
        early_share = pack_data.head(3)['Market_Share'].mean()
        if recent_share > early_share * 1.2:  # 20% growth in share
            emerging_packs.append((pack_type, recent_share/early_share))

if emerging_packs:
    print("\nEmerging Pack Types (Share Growth):")
    for pack_type, growth in sorted(emerging_packs, key=lambda x: x[1], reverse=True):
        print(f"  {pack_type}: {growth:.2f}x share growth")

# Regional growth patterns as leading indicator
regional_growth = df_long.groupby(['Month_Num', 'Region'])['Sales'].sum().reset_index()
growth_regions = []

for region in df_long['Region'].unique():
    region_data = regional_growth[regional_growth['Region'] == region].sort_values('Month_Num')
    if len(region_data) >= 6:
        recent_avg = region_data.tail(3)['Sales'].mean()
        early_avg = region_data.head(3)['Sales'].mean()
        if recent_avg > early_avg * 1.3:  # 30% growth
            growth_regions.append((region, recent_avg/early_avg))

if growth_regions:
    print("\nHigh-Growth Regions (Leading Indicators):")
    for region, growth in sorted(growth_regions, key=lambda x: x[1], reverse=True):
        print(f"  {region}: {growth:.2f}x growth rate")

# Early warning signs for competitors
print("\nB. Competitor Early Warning Signs:")

# Market share erosion detection
manu_monthly = df_long.groupby(['Month_Num', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
total_monthly_sales = df_long.groupby('Month_Num')['Sales'].sum()
manu_monthly['Market_Share'] = manu_monthly.apply(lambda x: x['Sales'] / total_monthly_sales.loc[x['Month_Num']] * 100, axis=1)

warnings = []
for manu in df_long['KEY MANU  & KINZA'].unique():
    manu_data = manu_monthly[manu_monthly['KEY MANU  & KINZA'] == manu].sort_values('Month_Num')
    if len(manu_data) >= 6:
        recent_share = manu_data.tail(3)['Market_Share'].mean()
        peak_share = manu_data['Market_Share'].max()
        if recent_share < peak_share * 0.9:  # 10% decline from peak
            warnings.append((manu, (peak_share - recent_share)))

if warnings:
    print("\nMarket Share Erosion Warnings:")
    for manu, decline in sorted(warnings, key=lambda x: x[1], reverse=True):
        print(f"  {manu}: {decline:.1f}% share decline from peak")

# Growth catalysts identification
print("\nC. Growth Catalysts:")

# Flavors driving regional growth
flavor_region_growth = df_long.groupby(['Region', 'CSD Flavor Segment', 'Month_Num'])['Sales'].sum().reset_index()
catalysts = []

for region in df_long['Region'].unique():
    region_data = flavor_region_growth[flavor_region_growth['Region'] == region]
    for flavor in region_data['CSD Flavor Segment'].unique():
        flavor_data = region_data[region_data['CSD Flavor Segment'] == flavor].sort_values('Month_Num')
        if len(flavor_data) >= 6:
            recent_avg = flavor_data.tail(3)['Sales'].mean()
            early_avg = flavor_data.head(3)['Sales'].mean()
            if recent_avg > early_avg * 1.5 and early_avg > 0:  # 50% growth
                catalysts.append((region, flavor, recent_avg/early_avg))

if catalysts:
    print("\nRegional Growth Catalysts:")
    for region, flavor, growth in sorted(catalysts, key=lambda x: x[2], reverse=True)[:5]:
        print(f"  {region} - {flavor}: {growth:.2f}x growth")

# 5. MARKET DYNAMICS
print("\n" + "=" * 60)
print("5. MARKET DYNAMICS")
print("=" * 60)

# Market elasticity patterns
print("\nA. Market Elasticity Patterns:")

# Price elasticity proxy through pack size analysis
pack_size_analysis = df_long.groupby(['Region', 'PACK SIZE'])['Sales'].sum().reset_index()
size_elasticity = []

for region in df_long['Region'].unique():
    region_data = pack_size_analysis[pack_size_analysis['Region'] == region].copy()
    # Extract numeric pack sizes
    region_data['Size_Numeric'] = region_data['PACK SIZE'].str.extract('(\d+)').astype(float)
    region_data = region_data.dropna(subset=['Size_Numeric'])
    
    if len(region_data) >= 3:
        # Simple elasticity: correlation between size and sales
        correlation = region_data['Size_Numeric'].corr(region_data['Sales'])
        if not np.isnan(correlation):
            size_elasticity.append((region, correlation))

print("Pack Size Elasticity by Region (Correlation Size vs Sales):")
for region, elasticity in sorted(size_elasticity, key=lambda x: abs(x[1]), reverse=True):
    print(f"  {region}: {elasticity:.3f}")

# Cannibalization effects
print("\nB. Cannibalization Effects:")

# Brand-2 analysis for cannibalization
brand_cannibalization = df_long.groupby(['Region', 'BRAND', 'Brand-2'])['Sales'].sum().reset_index()
cannibalization_effects = []

for region in df_long['Region'].unique():
    region_data = brand_cannibalization[brand_cannibalization['Region'] == region]
    for brand in region_data['BRAND'].unique():
        brand_data = region_data[region_data['BRAND'] == brand]
        brand_2_sales = brand_data[brand_data['Brand-2'] != '']['Sales'].sum()
        primary_sales = brand_data[brand_data['Brand-2'] == '']['Sales'].sum()
        
        if primary_sales > 0:
            cannibalization_rate = brand_2_sales / primary_sales * 100
            if cannibalization_rate > 10:  # Significant cannibalization
                cannibalization_effects.append((region, brand, cannibalization_rate))

if cannibalization_effects:
    print("\nHigh Cannibalization Effects (>10%):")
    for region, brand, rate in sorted(cannibalization_effects, key=lambda x: x[2], reverse=True)[:5]:
        print(f"  {region} - {brand}: {rate:.1f}% cannibalization")

# Price sensitivity indicators
print("\nC. Price Sensitivity Indicators:")

# Diet vs Regular as price sensitivity proxy
diet_regular_ratio = df_long.groupby('Region').apply(lambda x: 
    (x[x['REG/DIET'] == 'DIET']['Sales'].sum() / x[x['REG/DIET'] == 'REG']['Sales'].sum() * 100)
    if x[x['REG/DIET'] == 'REG']['Sales'].sum() > 0 else 0
).sort_values()

print("Diet/Regular Ratio by Region (Price Sensitivity Indicator):")
for region, ratio in diet_regular_ratio.items():
    print(f"  {region}: {ratio:.1f}%")

# Brand switching patterns
print("\nD. Brand Switching Patterns:")

# Pack type switching as brand switching proxy
pack_switching = df_long.groupby(['Region', 'PACK TYPE'])['Sales'].sum().reset_index()
pack_diversity = pack_switching.groupby('Region')['PACK TYPE'].nunique().sort_values()

print("Pack Type Diversity by Region (Brand Switching Proxy):")
for region, diversity in pack_diversity.items():
    print(f"  {region}: {diversity} pack types")

print("\n" + "=" * 80)
print("STRATEGIC RECOMMENDATIONS")
print("=" * 80)

print("\n**IMMEDIATE ACTIONS (0-3 months):**")
print(f"1. Address distribution gaps: {len(zero_analysis):,} zero-sales records need immediate attention")
print("2. Target low diet penetration regions for health-conscious consumer capture")
print("3. Leverage emerging pack types with strong growth momentum")
print("4. Monitor competitors showing market share erosion warnings")

print("\n**MEDIUM-TERM STRATEGIES (3-12 months):**")
print("1. Geographic expansion into top 5 opportunity provinces identified")
print("2. Portfolio optimization based on product lifecycle insights")
print("3. Seasonal inventory optimization for high-CV products")
print("4. Address cannibalization effects in high-impact regions")

print("\n**LONG-TERM INITIATIVES (12+ months):**")
print("1. Market elasticity-driven pricing strategy by region")
print("2. Brand switching reduction through loyalty programs")
print("3. Growth catalyst investment in high-potential regions")
print("4. Competitive positioning based on vulnerability analysis")

print("\n**COMPETITIVE ADVANTAGE OPPORTUNITIES:**")
print("1. First-mover advantage in emerging pack type segments")
print("2. White space capture in underserved flavor-region combinations")
print("3. Distribution superiority through gap elimination")
print("4. Data-driven seasonal optimization outperforming competitors")

print("\n**RISK MITIGATION:**")
print("1. Geographic diversification to reduce concentration risks")
print("2. Supplier diversification given manufacturer dominance")
print("3. Brand portfolio balance to reduce cannibalization")
print("4. Leading indicator monitoring for early threat detection")

print("\n" + "=" * 80)
print("STRATEGIC ANALYSIS COMPLETE")
print("=" * 80)