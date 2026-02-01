#!/usr/bin/env python3
"""
Exploratory Data Analysis Module
Saudi Arabian CSD Dataset Analysis Pipeline

This module provides comprehensive EDA functionality for market insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class CSDExploratoryAnalysis:
    """Comprehensive EDA for Saudi Arabian CSD dataset."""
    
    def __init__(self, df_long):
        """
        Initialize with long format dataset.
        
        Args:
            df_long (pd.DataFrame): Long format dataset
        """
        self.df = df_long.copy()
        self.setup_visualization()
        
    def setup_visualization(self):
        """Setup matplotlib and seaborn for better visualizations."""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
    def descriptive_statistics(self):
        """Generate comprehensive descriptive statistics."""
        print("=" * 80)
        print("DESCRIPTIVE STATISTICS")
        print("=" * 80)
        
        # Basic stats
        sales_stats = self.df['Sales'].describe()
        print("\nA. Sales Descriptive Statistics:")
        print(f"Count: {sales_stats['count']:,.0f}")
        print(f"Mean: {sales_stats['mean']:,.2f}")
        print(f"Std Dev: {sales_stats['std']:,.2f}")
        print(f"Min: {sales_stats['min']:,.2f}")
        print(f"25%: {sales_stats['25%']:,.2f}")
        print(f"Median: {sales_stats['50%']:,.2f}")
        print(f"75%: {sales_stats['75%']:,.2f}")
        print(f"Max: {sales_stats['max']:,.2f}")
        
        # Distribution analysis
        zero_sales = (self.df['Sales'] == 0).sum()
        positive_sales = (self.df['Sales'] > 0).sum()
        print(f"\nB. Distribution Analysis:")
        print(f"Zero Sales Records: {zero_sales:,} ({zero_sales/len(self.df)*100:.1f}%)")
        print(f"Positive Sales Records: {positive_sales:,} ({positive_sales/len(self.df)*100:.1f}%)")
        
        # Skewness and kurtosis
        skewness = stats.skew(self.df['Sales'])
        kurtosis = stats.kurtosis(self.df['Sales'])
        print(f"\nC. Distribution Shape:")
        print(f"Sales Skewness: {skewness:.2f} ({'Highly skewed' if abs(skewness) > 1 else 'Moderately skewed' if abs(skewness) > 0.5 else 'Approximately symmetric'})")
        print(f"Sales Kurtosis: {kurtosis:.2f} ({'Heavy-tailed' if kurtosis > 3 else 'Light-tailed' if kurtosis < 3 else 'Normal-like'})")
        
        return {
            'zero_sales_pct': zero_sales/len(self.df)*100,
            'skewness': skewness,
            'kurtosis': kurtosis,
            'mean_sales': sales_stats['mean'],
            'median_sales': sales_stats['50%']
        }
    
    def time_series_analysis(self):
        """Comprehensive time series analysis."""
        print("\n" + "=" * 80)
        print("TIME SERIES ANALYSIS")
        print("=" * 80)
        
        # Monthly trends
        monthly_total = self.df.groupby('Date')['Sales'].sum().reset_index()
        monthly_total['Month_Name'] = monthly_total['Date'].dt.strftime('%B')
        monthly_total['Sales_Millions'] = monthly_total['Sales'] / 1_000_000
        
        print("\nA. Monthly Sales Trends:")
        for _, row in monthly_total.iterrows():
            print(f"{row['Month_Name']:10s}: {row['Sales_Millions']:8.2f}M")
        
        # Seasonality metrics
        peak_month = monthly_total.loc[monthly_total['Sales'].idxmax()]
        low_month = monthly_total.loc[monthly_total['Sales'].idxmin()]
        seasonality_ratio = peak_month['Sales'] / low_month['Sales']
        
        print(f"\nB. Seasonality Analysis:")
        print(f"Peak Month: {peak_month['Month_Name']} ({peak_month['Sales_Millions']:.2f}M)")
        print(f"Lowest Month: {low_month['Month_Name']} ({low_month['Sales_Millions']:.2f}M)")
        print(f"Seasonality Ratio: {seasonality_ratio:.2f}x")
        
        # Growth and volatility
        monthly_total['Growth_Rate'] = monthly_total['Sales'].pct_change() * 100
        avg_growth_rate = monthly_total['Growth_Rate'].mean()
        cv = monthly_total['Sales'].std() / monthly_total['Sales'].mean()
        
        print(f"\nC. Growth & Volatility:")
        print(f"Average Monthly Growth Rate: {avg_growth_rate:.2f}%")
        print(f"Sales Volatility (CV): {cv:.2f} ({'High' if cv > 0.15 else 'Moderate' if cv > 0.10 else 'Low'})")
        
        # H1 vs H2 comparison
        h1_total = monthly_total[monthly_total['Date'].dt.month <= 6]['Sales'].sum()
        h2_total = monthly_total[monthly_total['Date'].dt.month > 6]['Sales'].sum()
        h1_h2_growth = (h2_total - h1_total) / h1_total * 100 if h1_total > 0 else 0
        
        print(f"\nD. Semi-Annual Comparison:")
        print(f"H1 Total (Jan-Jun): {h1_total/1_000_000:.2f}M")
        print(f"H2 Total (Jul-Dec): {h2_total/1_000_000:.2f}M")
        print(f"H2 vs H1 Growth: {h1_h2_growth:.2f}%")
        
        return {
            'seasonality_ratio': seasonality_ratio,
            'volatility': cv,
            'h2_vs_h1_growth': h1_h2_growth,
            'peak_month': peak_month['Month_Name'],
            'low_month': low_month['Month_Name']
        }
    
    def geographic_analysis(self):
        """Comprehensive geographic analysis."""
        print("\n" + "=" * 80)
        print("GEOGRAPHIC ANALYSIS")
        print("=" * 80)
        
        total_sales = self.df['Sales'].sum()
        
        # Regional performance
        regional_sales = self.df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        regional_sales_millions = regional_sales / 1_000_000
        
        print("\nA. Regional Performance:")
        for region, sales in regional_sales_millions.items():
            share = (sales / total_sales) * 100
            print(f"{region:20s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Province-level analysis (top 10)
        province_sales = self.df.groupby('Province')['Sales'].sum().sort_values(ascending=False)
        province_sales_millions = province_sales / 1_000_000
        
        print(f"\nB. Top 10 Provinces by Sales:")
        for i, (province, sales) in enumerate(province_sales_millions.head(10).items(), 1):
            share = (sales / total_sales) * 100
            print(f"{i:2d}. {province:20s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Geographic concentration (Herfindahl-Hirschman Index)
        regional_shares = regional_sales / total_sales
        hhi_regional = (regional_shares ** 2).sum()
        
        print(f"\nC. Geographic Concentration:")
        concentration_level = "High" if hhi_regional > 0.25 else "Moderate" if hhi_regional > 0.15 else "Low"
        print(f"Regional HHI: {hhi_regional:.4f} ({concentration_level} concentration)")
        
        return {
            'hhi_regional': hhi_regional,
            'concentration_level': concentration_level,
            'top_region': regional_sales.index[0],
            'region_market_share': (regional_sales.iloc[0] / total_sales) * 100
        }
    
    def product_performance_analysis(self):
        """Comprehensive product performance analysis."""
        print("\n" + "=" * 80)
        print("PRODUCT PERFORMANCE ANALYSIS")
        print("=" * 80)
        
        total_sales = self.df['Sales'].sum()
        
        # Manufacturer market share
        manu_sales = self.df.groupby('KEY MANU  & KINZA')['Sales'].sum().sort_values(ascending=False)
        manu_sales_millions = manu_sales / 1_000_000
        
        print("\nA. Manufacturer Market Share:")
        for manu, sales in manu_sales_millions.items():
            share = (sales / total_sales) * 100
            print(f"{manu:20s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Brand performance (top 15)
        brand_sales = self.df.groupby('BRAND')['Sales'].sum().sort_values(ascending=False)
        brand_sales_millions = brand_sales / 1_000_000
        
        print(f"\nB. Top 15 Brands by Sales:")
        for i, (brand, sales) in enumerate(brand_sales_millions.head(15).items(), 1):
            share = (sales / total_sales) * 100
            print(f"{i:2d}. {brand:20s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Flavor segment analysis
        flavor_sales = self.df.groupby('CSD Flavor Segment')['Sales'].sum().sort_values(ascending=False)
        flavor_sales_millions = flavor_sales / 1_000_000
        
        print(f"\nC. Flavor Segment Preferences:")
        for flavor, sales in flavor_sales_millions.items():
            share = (sales / total_sales) * 100
            print(f"{flavor:15s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Pack type analysis
        pack_type_sales = self.df.groupby('PACK TYPE')['Sales'].sum().sort_values(ascending=False)
        pack_type_sales_millions = pack_type_sales / 1_000_000
        
        print(f"\nD. Pack Type Performance:")
        for pack_type, sales in pack_type_sales_millions.items():
            share = (sales / total_sales) * 100
            print(f"{pack_type:10s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Regular vs Diet
        reg_diet_sales = self.df.groupby('REG/DIET')['Sales'].sum().sort_values(ascending=False)
        reg_diet_sales_millions = reg_diet_sales / 1_000_000
        
        print(f"\nE. Regular vs Diet Preferences:")
        for reg_diet, sales in reg_diet_sales_millions.items():
            share = (sales / total_sales) * 100
            print(f"{reg_diet:8s}: {sales:8.2f}M ({share:5.1f}%)")
        
        return {
            'top_manufacturer': manu_sales.index[0],
            'top_manufacturer_share': (manu_sales.iloc[0] / total_sales) * 100,
            'top_brand': brand_sales.index[0],
            'top_flavor': flavor_sales.index[0],
            'top_pack_type': pack_type_sales.index[0],
            'diet_penetration': (reg_diet_sales.get('DIET', 0) / total_sales) * 100
        }
    
    def correlation_analysis(self):
        """Analyze correlations between different dimensions."""
        print("\n" + "=" * 80)
        print("CORRELATION ANALYSIS")
        print("=" * 80)
        
        # Monthly sales correlation matrix
        monthly_pivot = self.df.pivot_table(values='Sales', index='Region', columns='Month', aggfunc='sum')
        correlation_matrix = monthly_pivot.corr()
        avg_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
        
        print(f"A. Monthly Sales Correlation:")
        print(f"Average Monthly Correlation: {avg_correlation:.3f} ({'High' if avg_correlation > 0.7 else 'Moderate' if avg_correlation > 0.3 else 'Low'})")
        
        # Top correlations
        correlations = []
        months = monthly_pivot.columns.tolist()
        for i in range(len(months)):
            for j in range(i+1, len(months)):
                corr_val = correlation_matrix.iloc[i, j]
                correlations.append((months[i], months[j], corr_val))
        
        correlations.sort(key=lambda x: abs(x[2]), reverse=True)
        print("Top 5 Monthly Correlations:")
        for month1, month2, corr in correlations[:5]:
            print(f"  {month1} ↔ {month2}: {corr:.3f}")
        
        return {
            'avg_monthly_correlation': avg_correlation,
            'correlation_level': 'High' if avg_correlation > 0.7 else 'Moderate' if avg_correlation > 0.3 else 'Low'
        }
    
    def generate_insights(self):
        """Generate key business insights from analysis."""
        print("\n" + "=" * 80)
        print("KEY BUSINESS INSIGHTS")
        print("=" * 80)
        
        # Run all analyses
        desc_stats = self.descriptive_statistics()
        ts_analysis = self.time_series_analysis()
        geo_analysis = self.geographic_analysis()
        prod_analysis = self.product_performance_analysis()
        corr_analysis = self.correlation_analysis()
        
        # Synthesize insights
        insights = {
            'market_size': self.df['Sales'].sum() / 1_000_000,
            'data_quality': {
                'zero_sales_pct': desc_stats['zero_sales_pct'],
                'skewness': desc_stats['skewness']
            },
            'seasonality': {
                'peak_month': ts_analysis['peak_month'],
                'seasonality_ratio': ts_analysis['seasonality_ratio'],
                'volatility': ts_analysis['volatility']
            },
            'geography': {
                'concentration_level': geo_analysis['concentration_level'],
                'hhi': geo_analysis['hhi_regional'],
                'top_region': geo_analysis['top_region']
            },
            'products': {
                'top_manufacturer': prod_analysis['top_manufacturer'],
                'top_manufacturer_share': prod_analysis['top_manufacturer_share'],
                'diet_penetration': prod_analysis['diet_penetration']
            },
            'correlations': corr_analysis['avg_monthly_correlation']
        }
        
        print("\n📊 MARKET OVERVIEW:")
        print(f"• Total Market Size: {insights['market_size']:.1f}M SAR annually")
        print(f"• Data Quality: {100-insights['data_quality']['zero_sales_pct']:.1f}% complete records")
        
        print("\n📈 SEASONALITY:")
        print(f"• Peak Month: {insights['seasonality']['peak_month']}")
        print(f"• Seasonality Ratio: {insights['seasonality']['seasonality_ratio']:.1f}x")
        print(f"• Volatility: {insights['seasonality']['volatility']:.2f} ({'High' if insights['seasonality']['volatility'] > 0.15 else 'Moderate'})")
        
        print("\n🌍 GEOGRAPHIC CONCENTRATION:")
        print(f"• Market Concentration: {insights['geography']['concentration_level']} (HHI: {insights['geography']['hhi']:.3f})")
        print(f"• Top Region: {insights['geography']['top_region']}")
        
        print("\n🥤 PRODUCT LANDSCAPE:")
        print(f"• Market Leader: {insights['products']['top_manufacturer']} ({insights['products']['top_manufacturer_share']:.1f}% share)")
        print(f"• Diet Segment Penetration: {insights['products']['diet_penetration']:.1f}%")
        
        return insights

def main():
    """Example usage of the EDA module."""
    # This would be used with the data loader
    # loader = CSDDatasetLoader()
    # loader.load_data()
    # loader.convert_to_long_format()
    # loader.clean_data()
    # loader.create_derived_features()
    
    # analyzer = CSDExploratoryAnalysis(loader.df_long)
    # insights = analyzer.generate_insights()
    
    print("CSD Exploratory Analysis Module Ready!")
    print("Use with CSDDatasetLoader to analyze your dataset.")

if __name__ == "__main__":
    main()