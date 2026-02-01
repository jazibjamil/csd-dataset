#!/usr/bin/env python3
"""
Time Series Analysis Module
Saudi Arabian CSD Dataset Analysis Pipeline

This module provides comprehensive time series and seasonal analysis capabilities.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class CSDTimeSeriesAnalysis:
    """Comprehensive time series analysis for seasonal patterns and forecasting."""
    
    def __init__(self, df_long):
        """
        Initialize with long format dataset.
        
        Args:
            df_long (pd.DataFrame): Long format dataset
        """
        self.df = df_long.copy()
        
    def seasonal_decomposition(self):
        """Analyze seasonal patterns and decomposition."""
        print("=" * 80)
        print("SEASONAL DECOMPOSITION ANALYSIS")
        print("=" * 80)
        
        # Overall monthly patterns
        monthly_total = self.df.groupby('Date')['Sales'].sum().reset_index()
        monthly_total['Month_Name'] = monthly_total['Date'].dt.strftime('%B')
        monthly_total['Sales_Millions'] = monthly_total['Sales'] / 1_000_000
        
        print(f"\n📊 Monthly Sales Pattern (Millions SAR):")
        for _, row in monthly_total.iterrows():
            print(f"  {row['Month_Name']:10s}: {row['Sales_Millions']:8.2f}M")
        
        # Seasonality metrics
        peak_month = monthly_total.loc[monthly_total['Sales'].idxmax()]
        low_month = monthly_total.loc[monthly_total['Sales'].idxmin()]
        seasonality_ratio = peak_month['Sales'] / low_month['Sales']
        
        print(f"\n🌡️ Seasonality Analysis:")
        print(f"• Peak Month: {peak_month['Month_Name']} ({peak_month['Sales_Millions']:.2f}M)")
        print(f"• Lowest Month: {low_month['Month_Name']} ({low_month['Sales_Millions']:.2f}M)")
        print(f"• Seasonality Ratio: {seasonality_ratio:.2f}x")
        
        # Volatility analysis
        monthly_total['Growth_Rate'] = monthly_total['Sales'].pct_change() * 100
        cv = monthly_total['Sales'].std() / monthly_total['Sales'].mean()
        avg_growth_rate = monthly_total['Growth_Rate'].mean()
        
        print(f"\n📈 Volatility & Growth:")
        print(f"• Average Monthly Growth: {avg_growth_rate:.2f}%")
        print(f"• Coefficient of Variation: {cv:.3f}")
        volatility_level = "HIGH" if cv > 0.15 else "MODERATE" if cv > 0.10 else "LOW"
        print(f"• Volatility Level: {volatility_level}")
        
        # H1 vs H2 comparison
        h1_total = monthly_total[monthly_total['Date'].dt.month <= 6]['Sales'].sum()
        h2_total = monthly_total[monthly_total['Date'].dt.month > 6]['Sales'].sum()
        h1_h2_growth = (h2_total - h1_total) / h1_total * 100 if h1_total > 0 else 0
        
        print(f"\n📅 Semi-Annual Performance:")
        print(f"• H1 (Jan-Jun): {h1_total/1_000_000:.2f}M")
        print(f"• H2 (Jul-Dec): {h2_total/1_000_000:.2f}M")
        print(f"• H2 vs H1 Growth: {h1_h2_growth:.2f}%")
        
        return {
            'peak_month': peak_month['Month_Name'],
            'low_month': low_month['Month_Name'],
            'seasonality_ratio': seasonality_ratio,
            'volatility': cv,
            'h2_vs_h1_growth': h1_h2_growth
        }
    
    def regional_seasonal_patterns(self):
        """Analyze seasonal patterns by region."""
        print("\n" + "=" * 80)
        print("REGIONAL SEASONAL PATTERNS")
        print("=" * 80)
        
        # Regional seasonal analysis
        regional_seasonal = self.df.groupby(['Region', 'Season'])['Sales'].sum().reset_index()
        regional_seasonal_pivot = regional_seasonal.pivot(index='Region', columns='Season', values='Sales').fillna(0)
        
        print(f"\n🌍 Regional Seasonal Distribution (% of regional sales):")
        for region in regional_seasonal_pivot.index:
            winter = regional_seasonal_pivot.loc[region, 'Winter']
            spring = regional_seasonal_pivot.loc[region, 'Spring']
            summer = regional_seasonal_pivot.loc[region, 'Summer']
            fall = regional_seasonal_pivot.loc[region, 'Fall']
            total = winter + spring + summer + fall
            
            if total > 0:
                print(f"  {region:20s}: Winter {winter/total*100:5.1f}% | "
                      f"Spring {spring/total*100:5.1f}% | "
                      f"Summer {summer/total*100:5.1f}% | "
                      f"Fall {fall/total*100:5.1f}%")
        
        # Peak month analysis by region
        print(f"\n🎯 Regional Peak Months:")
        regional_monthly = self.df.groupby(['Region', 'Month_Name'])['Sales'].sum().reset_index()
        peak_months = []
        
        for region in self.df['Region'].unique():
            region_data = regional_monthly[regional_monthly['Region'] == region]
            peak_month_region = region_data.loc[region_data['Sales'].idxmax(), 'Month_Name']
            total_region_sales = region_data['Sales'].sum()
            peak_share = (region_data['Sales'].max() / total_region_sales) * 100
            peak_months.append((region, peak_month_region, peak_share))
        
        peak_months.sort(key=lambda x: x[2], reverse=True)
        print("Regional Peak Months and Concentration:")
        for region, peak_month, peak_share in peak_months:
            concentration = "HIGH" if peak_share > 15 else "MODERATE" if peak_share > 10 else "LOW"
            print(f"  {region:20s}: {peak_month:10s} ({peak_share:5.1f}% of annual sales) [{concentration}]")
        
        return {
            'most_seasonal_region': peak_months[0][0] if peak_months else None,
            'regional_peak_variance': max([pm[2] for pm in peak_months]) - min([pm[2] for pm in peak_months]) if peak_months else 0
        }
    
    def product_seasonal_analysis(self):
        """Analyze seasonal patterns by product categories."""
        print("\n" + "=" * 80)
        print("PRODUCT SEASONAL ANALYSIS")
        print("=" * 80)
        
        # Flavor seasonal patterns
        flavor_seasonal = self.df.groupby(['CSD Flavor Segment', 'Season'])['Sales'].sum().reset_index()
        flavor_seasonal_pivot = flavor_seasonal.pivot(index='CSD Flavor Segment', columns='Season', values='Sales').fillna(0)
        
        print(f"\n🍋 Flavor Seasonal Patterns (% of flavor sales):")
        for flavor in flavor_seasonal_pivot.index:
            winter = flavor_seasonal_pivot.loc[flavor, 'Winter']
            spring = flavor_seasonal_pivot.loc[flavor, 'Spring']
            summer = flavor_seasonal_pivot.loc[flavor, 'Summer']
            fall = flavor_seasonal_pivot.loc[flavor, 'Fall']
            total = winter + spring + summer + fall
            
            if total > 0:
                print(f"  {flavor:15s}: Winter {winter/total*100:5.1f}% | "
                      f"Spring {spring/total*100:5.1f}% | "
                      f"Summer {summer/total*100:5.1f}% | "
                      f"Fall {fall/total*100:5.1f}%")
        
        # Pack type seasonal patterns
        pack_seasonal = self.df.groupby(['PACK TYPE', 'Season'])['Sales'].sum().reset_index()
        pack_seasonal_pivot = pack_seasonal.pivot(index='PACK TYPE', columns='Season', values='Sales').fillna(0)
        
        print(f"\n📦 Pack Type Seasonal Patterns (% of pack type sales):")
        for pack_type in pack_seasonal_pivot.index:
            winter = pack_seasonal_pivot.loc[pack_type, 'Winter']
            spring = pack_seasonal_pivot.loc[pack_type, 'Spring']
            summer = pack_seasonal_pivot.loc[pack_type, 'Summer']
            fall = pack_seasonal_pivot.loc[pack_type, 'Fall']
            total = winter + spring + summer + fall
            
            if total > 0:
                print(f"  {pack_type:15s}: Winter {winter/total*100:5.1f}% | "
                      f"Spring {spring/total*100:5.1f}% | "
                      f"Summer {summer/total*100:5.1f}% | "
                      f"Fall {fall/total*100:5.1f}%")
        
        # Diet vs Regular seasonal patterns
        reg_diet_seasonal = self.df.groupby(['REG/DIET', 'Season'])['Sales'].sum().reset_index()
        reg_diet_seasonal_pivot = reg_diet_seasonal.pivot(index='REG/DIET', columns='Season', values='Sales').fillna(0)
        
        print(f"\n🥤 Regular vs Diet Seasonal Patterns (% of segment sales):")
        for segment in reg_diet_seasonal_pivot.index:
            winter = reg_diet_seasonal_pivot.loc[segment, 'Winter']
            spring = reg_diet_seasonal_pivot.loc[segment, 'Spring']
            summer = reg_diet_seasonal_pivot.loc[segment, 'Summer']
            fall = reg_diet_seasonal_pivot.loc[segment, 'Fall']
            total = winter + spring + summer + fall
            
            if total > 0:
                print(f"  {segment:8s}: Winter {winter/total*100:5.1f}% | "
                      f"Spring {spring/total*100:5.1f}% | "
                      f"Summer {summer/total*100:5.1f}% | "
                      f"Fall {fall/total*100:5.1f}%")
        
        return {
            'most_seasonal_flavor': flavor_seasonal_pivot.index[0] if len(flavor_seasonal_pivot) > 0 else None,
            'most_seasonal_pack': pack_seasonal_pivot.index[0] if len(pack_seasonal_pivot) > 0 else None
        }
    
    def trend_analysis(self):
        """Analyze growth trends and patterns."""
        print("\n" + "=" * 80)
        print("TREND ANALYSIS")
        print("=" * 80)
        
        # Overall trend analysis
        monthly_total = self.df.groupby('Date')['Sales'].sum().reset_index()
        monthly_total['Month_Num'] = monthly_total['Date'].dt.month
        
        # Calculate moving averages
        monthly_total['MA_3'] = monthly_total['Sales'].rolling(window=3).mean()
        monthly_total['MA_6'] = monthly_total['Sales'].rolling(window=6).mean()
        
        print(f"\n📈 Trend Analysis (Sales in Millions SAR):")
        for _, row in monthly_total.iterrows():
            ma3_val = row['MA_3'] / 1_000_000 if pd.notna(row['MA_3']) else 0
            ma6_val = row['MA_6'] / 1_000_000 if pd.notna(row['MA_6']) else 0
            print(f"  {row['Date'].strftime('%b'):3s}: "
                  f"{row['Sales']/1_000_000:7.2f}M | "
                  f"3MA: {ma3_val:7.2f}M | "
                  f"6MA: {ma6_val:7.2f}M")
        
        # Growth momentum analysis
        monthly_total['Growth_Rate'] = monthly_total['Sales'].pct_change() * 100
        monthly_total['Momentum'] = monthly_total['Growth_Rate'].rolling(window=3).mean()
        
        print(f"\n🚀 Growth Momentum:")
        momentum_periods = []
        for _, row in monthly_total.iterrows():
            if pd.notna(row['Momentum']):
                momentum_level = "STRONG" if row['Momentum'] > 10 else "POSITIVE" if row['Momentum'] > 0 else "NEGATIVE"
                momentum_periods.append((row['Date'].strftime('%b'), row['Momentum'], momentum_level))
        
        for month, momentum, level in momentum_periods:
            print(f"  {month:3s}: {momentum:+6.1f}% [{level}]")
        
        # Manufacturer trend analysis
        print(f"\n🏆 Manufacturer Trend Analysis:")
        manu_monthly = self.df.groupby(['Month_Num', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
        manu_trends = []
        
        for manu in self.df['KEY MANU  & KINZA'].unique():
            manu_data = manu_monthly[manu_monthly['KEY MANU  & KINZA'] == manu].sort_values('Month_Num')
            if len(manu_data) >= 6:
                early_avg = manu_data.head(3)['Sales'].mean()
                recent_avg = manu_data.tail(3)['Sales'].mean()
                if early_avg > 0:
                    growth_rate = ((recent_avg - early_avg) / early_avg) * 100
                    manu_trends.append((manu, growth_rate))
        
        manu_trends.sort(key=lambda x: x[1], reverse=True)
        print("Manufacturer Growth Rates (H2 vs H1):")
        for manu, growth in manu_trends:
            trend = "SURGING" if growth > 30 else "GROWING" if growth > 10 else "STABLE" if growth > -10 else "DECLINING"
            print(f"  {manu:15s}: {growth:+6.1f}% [{trend}]")
        
        return {
            'overall_momentum': momentum_periods[-1][1] if momentum_periods else 0,
            'top_growth_manufacturer': manu_trends[0][0] if manu_trends else None,
            'top_growth_rate': manu_trends[0][1] if manu_trends else 0
        }
    
    def ramadan_impact_analysis(self):
        """Analyze Ramadan impact on sales patterns."""
        print("\n" + "=" * 80)
        print("RAMADAN IMPACT ANALYSIS")
        print("=" * 80)
        
        # Overall Ramadan impact
        ramadan_data = self.df.groupby(['Ramadan_Period', 'Month_Num'])['Sales'].sum().reset_index()
        ramadan_month = ramadan_data[ramadan_data['Ramadan_Period'] == 1]
        non_ramadan_data = ramadan_data[ramadan_data['Ramadan_Period'] == 0]
        
        if not ramadan_month.empty:
            ramadan_sales = ramadan_month['Sales'].iloc[0]
            avg_non_ramadan = non_ramadan_data['Sales'].mean()
            ramadan_impact = ((ramadan_sales - avg_non_ramadan) / avg_non_ramadan) * 100 if avg_non_ramadan > 0 else 0
            
            print(f"\n🕌 Overall Ramadan Impact:")
            print(f"• Ramadan Sales: {ramadan_sales/1_000_000:.2f}M")
            print(f"• Average Non-Ramadan Month: {avg_non_ramadan/1_000_000:.2f}M")
            print(f"• Ramadan Impact: {ramadan_impact:+.1f}% vs average")
            
            impact_level = "EXTREME" if ramadan_impact > 50 else "HIGH" if ramadan_impact > 25 else "MODERATE" if ramadan_impact > 10 else "LOW"
            print(f"• Impact Level: {impact_level}")
        else:
            print(f"\n🕌 No Ramadan period identified in the data")
            ramadan_impact = 0
        
        # Regional Ramadan impact
        regional_ramadan = self.df.groupby(['Region', 'Ramadan_Period'])['Sales'].sum().reset_index()
        regional_ramadan_pivot = regional_ramadan.pivot(index='Region', columns='Ramadan_Period', values='Sales').fillna(0)
        
        print(f"\n🌍 Regional Ramadan Impact:")
        ramadan_impacts = []
        for region in regional_ramadan_pivot.index:
            ramadan_sales = regional_ramadan_pivot.loc[region, 1] if 1 in regional_ramadan_pivot.columns else 0
            non_ramadan_sales = regional_ramadan_pivot.loc[region, 0] if 0 in regional_ramadan_pivot.columns else 0
            
            if non_ramadan_sales > 0:
                # Normalize by months
                ramadan_avg = ramadan_sales / 1
                non_ramadan_avg = non_ramadan_sales / 11
                impact = ((ramadan_avg - non_ramadan_avg) / non_ramadan_avg) * 100
                ramadan_impacts.append((region, impact))
        
        ramadan_impacts.sort(key=lambda x: x[1], reverse=True)
        print("Regional Ramadan Impact (% vs average month):")
        for region, impact in ramadan_impacts:
            sensitivity = "HIGHLY SENSITIVE" if impact > 50 else "SENSITIVE" if impact > 25 else "MODERATE" if impact > 10 else "LOW"
            print(f"  {region:20s}: {impact:+6.1f}% [{sensitivity}]")
        
        # Product category Ramadan impact
        print(f"\n🥤 Product Category Ramadan Impact:")
        category_ramadan = self.df.groupby(['CSD Flavor Segment', 'Ramadan_Period'])['Sales'].sum().reset_index()
        category_ramadan_pivot = category_ramadan.pivot(index='CSD Flavor Segment', columns='Ramadan_Period', values='Sales').fillna(0)
        
        category_impacts = []
        for category in category_ramadan_pivot.index:
            ramadan_sales = category_ramadan_pivot.loc[category, 1] if 1 in category_ramadan_pivot.columns else 0
            non_ramadan_sales = category_ramadan_pivot.loc[category, 0] if 0 in category_ramadan_pivot.columns else 0
            
            if non_ramadan_sales > 0:
                ramadan_avg = ramadan_sales / 1
                non_ramadan_avg = non_ramadan_sales / 11
                impact = ((ramadan_avg - non_ramadan_avg) / non_ramadan_avg) * 100
                category_impacts.append((category, impact))
        
        category_impacts.sort(key=lambda x: x[1], reverse=True)
        print("Flavor Segment Ramadan Impact (% vs average month):")
        for category, impact in category_impacts:
            print(f"  {category:15s}: {impact:+6.1f}%")
        
        return {
            'overall_ramadan_impact': ramadan_impact,
            'highest_ramadan_region': ramadan_impacts[0][0] if ramadan_impacts else None,
            'highest_ramadan_impact': ramadan_impacts[0][1] if ramadan_impacts else 0
        }
    
    def generate_temporal_intelligence(self):
        """Generate comprehensive temporal intelligence report."""
        print("\n" + "=" * 80)
        print("TEMPORAL INTELLIGENCE SUMMARY")
        print("=" * 80)
        
        # Run all analyses
        seasonal = self.seasonal_decomposition()
        regional_seasonal = self.regional_seasonal_patterns()
        product_seasonal = self.product_seasonal_analysis()
        trends = self.trend_analysis()
        ramadan = self.ramadan_impact_analysis()
        
        # Key insights
        print(f"\n📅 TEMPORAL STRATEGIC INSIGHTS:")
        print(f"• Peak Season: {seasonal['peak_month']} ({seasonal['seasonality_ratio']:.1f}x over low month)")
        print(f"• Market Volatility: {seasonal['volatility']:.3f} ({'HIGH' if seasonal['volatility'] > 0.15 else 'MODERATE'})")
        print(f"• H2 vs H1 Growth: {seasonal['h2_vs_h1_growth']:+.1f}%")
        
        if trends['overall_momentum'] != 0:
            momentum_dir = "POSITIVE" if trends['overall_momentum'] > 0 else "NEGATIVE"
            print(f"• Growth Momentum: {trends['overall_momentum']:+.1f}% ({momentum_dir})")
        
        if ramadan['overall_ramadan_impact'] != 0:
            print(f"• Ramadan Impact: {ramadan['overall_ramadan_impact']:+.1f}% vs average")
        
        # Strategic recommendations
        print(f"\n🎯 TEMPORAL STRATEGIC RECOMMENDATIONS:")
        
        if seasonal['seasonality_ratio'] > 1.5:
            print(f"1. OPTIMIZE: Strong seasonality ({seasonal['seasonality_ratio']:.1f}x) requires targeted inventory planning")
        
        if seasonal['h2_vs_h1_growth'] > 10:
            print(f"2. CAPITALIZE: H2 strength ({seasonal['h2_vs_h1_growth']:+.1f}%) suggests holiday/Ramadan focus")
        
        if ramadan['overall_ramadan_impact'] > 25:
            print(f"3. FOCUS: High Ramadan sensitivity ({ramadan['overall_ramadan_impact']:+.1f}%) requires special programming")
        
        if trends['top_growth_rate'] > 20:
            print(f"4. SCALE: {trends['top_growth_manufacturer']} showing strong momentum ({trends['top_growth_rate']:+.1f}%)")
        
        print(f"5. FORECAST: Use seasonal patterns for demand planning and inventory optimization")
        
        return {
            'peak_season': seasonal['peak_month'],
            'volatility_level': seasonal['volatility'],
            'growth_momentum': trends['overall_momentum'],
            'ramadan_sensitivity': abs(ramadan['overall_ramadan_impact']),
            'strategic_priority': "HIGH" if seasonal['seasonality_ratio'] > 1.5 else "MEDIUM"
        }

def main():
    """Example usage of the time series analysis module."""
    print("CSD Time Series Analysis Module Ready!")
    print("Use with CSDDatasetLoader to analyze temporal patterns.")

if __name__ == "__main__":
    main()