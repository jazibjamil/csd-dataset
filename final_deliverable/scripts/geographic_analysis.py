#!/usr/bin/env python3
"""
Geographic Analysis Module
Saudi Arabian CSD Dataset Analysis Pipeline

This module provides comprehensive geographic and regional analysis capabilities.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class CSDGeographicAnalysis:
    """Comprehensive geographic analysis for market intelligence."""
    
    def __init__(self, df_long):
        """
        Initialize with long format dataset.
        
        Args:
            df_long (pd.DataFrame): Long format dataset
        """
        self.df = df_long.copy()
        
    def regional_performance_analysis(self):
        """Analyze regional performance and market dynamics."""
        print("=" * 80)
        print("REGIONAL PERFORMANCE ANALYSIS")
        print("=" * 80)
        
        total_sales = self.df['Sales'].sum()
        
        # Regional sales performance
        regional_sales = self.df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        regional_sales_millions = regional_sales / 1_000_000
        
        print(f"\n📊 Regional Sales Performance:")
        for region, sales in regional_sales_millions.items():
            share = (sales / total_sales) * 100
            tier = "TIER 1" if share > 20 else "TIER 2" if share > 10 else "TIER 3" if share > 5 else "TIER 4"
            print(f"  {region:20s}: {sales:8.2f}M ({share:5.1f}%) [{tier}]")
        
        # Regional growth patterns
        print(f"\n📈 Regional Growth Patterns:")
        regional_growth = self.df.groupby(['Region', 'Month_Num'])['Sales'].sum().reset_index()
        growth_analysis = []
        
        for region in self.df['Region'].unique():
            region_data = regional_growth[regional_growth['Region'] == region].sort_values('Month_Num')
            if len(region_data) >= 6:
                recent_avg = region_data.tail(3)['Sales'].mean()
                early_avg = region_data.head(3)['Sales'].mean()
                if early_avg > 0:
                    growth_rate = ((recent_avg - early_avg) / early_avg) * 100
                    growth_analysis.append((region, growth_rate))
        
        growth_analysis.sort(key=lambda x: x[1], reverse=True)
        print("Regional Growth Rates (H2 vs H1):")
        for region, growth in growth_analysis:
            momentum = "EXPLOSIVE" if growth > 50 else "STRONG" if growth > 20 else "MODERATE" if growth > 0 else "DECLINING"
            print(f"  {region:20s}: {growth:+6.1f}% [{momentum}]")
        
        return {
            'top_region': regional_sales.index[0],
            'top_region_share': (regional_sales.iloc[0] / total_sales) * 100,
            'growth_leaders': [g[0] for g in growth_analysis if g[1] > 20],
            'declining_regions': [g[0] for g in growth_analysis if g[1] < -10]
        }
    
    def province_level_deep_dive(self):
        """Deep dive into province-level analysis."""
        print("\n" + "=" * 80)
        print("PROVINCE-LEVEL DEEP DIVE")
        print("=" * 80)
        
        total_sales = self.df['Sales'].sum()
        
        # Province performance metrics
        province_sales = self.df.groupby('Province')['Sales'].sum().sort_values(ascending=False)
        province_sales_millions = province_sales / 1_000_000
        
        print(f"\n🏆 Top 15 Provinces by Sales:")
        for i, (province, sales) in enumerate(province_sales_millions.head(15).items(), 1):
            share = (sales / total_sales) * 100
            print(f"  {i:2d}. {province:20s}: {sales:8.2f}M ({share:5.1f}%)")
        
        # Province opportunity scoring
        province_metrics = self.df.groupby('Province').agg({
            'Sales': 'sum',
            'Precision Area': 'nunique',
            'BRAND': 'nunique',
            'MARKET': 'nunique'
        }).reset_index()
        
        province_metrics['Sales_Per_Area'] = province_metrics['Sales'] / province_metrics['Precision Area']
        province_metrics['Brand_Density'] = province_metrics['BRAND'] / province_metrics['Precision Area']
        province_metrics['Market_Density'] = province_metrics['MARKET'] / province_metrics['Precision Area']
        
        # Opportunity score (inverse of current performance)
        province_metrics['Opportunity_Score'] = (
            province_metrics['Sales_Per_Area'].rank(ascending=True) * 0.3 +
            province_metrics['Brand_Density'].rank(ascending=True) * 0.3 +
            province_metrics['Market_Density'].rank(ascending=True) * 0.2 +
            province_metrics['Sales'].rank(ascending=True) * 0.2
        )
        
        print(f"\n🎯 Top 10 Provinces for Expansion (Opportunity Score):")
        top_opportunities = province_metrics.nlargest(10, 'Opportunity_Score')
        for _, row in top_opportunities.iterrows():
            potential = "HIGH" if row['Opportunity_Score'] > 30 else "MEDIUM" if row['Opportunity_Score'] > 20 else "LOW"
            print(f"  {row['Province']:20s}: Score {row['Opportunity_Score']:4.1f} | "
                  f"{row['Sales']/1_000_000:6.2f}M sales, {row['Precision Area']:2.0f} areas [{potential}]")
        
        # Province concentration analysis
        print(f"\n🏘️ Province Market Concentration:")
        province_manu = self.df.groupby(['Province', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
        province_totals = province_manu.groupby('Province')['Sales'].sum()
        
        concentration_risks = []
        for province in self.df['Province'].unique():
            province_manu_data = province_manu[province_manu['Province'] == province]
            province_total = province_totals[province]
            province_manu_data['Share'] = province_manu_data['Sales'] / province_total * 100
            
            top_share = province_manu_data['Share'].max()
            if top_share > 80:
                top_manu = province_manu_data.loc[province_manu_data['Share'].idxmax(), 'KEY MANU  & KINZA']
                concentration_risks.append((province, top_manu, top_share))
        
        if concentration_risks:
            print("High Concentration Provinces (>80% share):")
            for province, manu, share in sorted(concentration_risks, key=lambda x: x[2], reverse=True):
                print(f"  {province:20s}: {manu:15s} dominates with {share:.1f}%")
        else:
            print("✅ No critical concentration risks at province level")
        
        return {
            'top_province': province_sales.index[0],
            'top_expansion_province': top_opportunities.iloc[0]['Province'],
            'opportunity_score': top_opportunities.iloc[0]['Opportunity_Score'],
            'concentration_risks': len(concentration_risks)
        }
    
    def precision_area_hotspot_analysis(self):
        """Analyze precision areas for hotspots and coldspots."""
        print("\n" + "=" * 80)
        print("PRECISION AREA HOTSPOT ANALYSIS")
        print("=" * 80)
        
        total_sales = self.df['Sales'].sum()
        
        # Precision area performance
        precision_sales = self.df.groupby('Precision Area')['Sales'].sum().sort_values(ascending=False)
        precision_sales_millions = precision_sales / 1_000_000
        
        print(f"\n🔥 Top 20 Precision Areas (Hotspots):")
        for i, (area, sales) in enumerate(precision_sales_millions.head(20).items(), 1):
            share = (sales / total_sales) * 100
            hotspot_level = "MEGA" if share > 3 else "MAJOR" if share > 2 else "SIGNIFICANT" if share > 1 else "GROWING"
            print(f"  {i:2d}. {area:25s}: {sales:7.3f}M ({share:4.2f}%) [{hotspot_level}]")
        
        # Coldspot analysis (areas with potential)
        precision_area_metrics = self.df.groupby('Precision Area').agg({
            'Sales': 'sum',
            'Region': 'nunique',
            'BRAND': 'nunique',
            'Month_Num': 'nunique'
        }).reset_index()
        
        # Identify areas with low sales but good fundamentals
        precision_area_metrics['Avg_Monthly_Sales'] = precision_area_metrics['Sales'] / precision_area_metrics['Month_Num']
        precision_area_metrics['Brand_Competition'] = precision_area_metrics['BRAND']
        
        # Coldspot score (low current sales, high potential)
        precision_area_metrics['Coldspot_Score'] = (
            precision_area_metrics['Sales'].rank(ascending=True) * 0.4 +
            precision_area_metrics['Brand_Competition'].rank(ascending=False) * 0.3 +
            precision_area_metrics['Avg_Monthly_Sales'].rank(ascending=False) * 0.3
        )
        
        print(f"\n❄️ Top 10 Precision Areas for Development (Coldspots):")
        coldspots = precision_area_metrics.nsmallest(10, 'Coldspot_Score')
        for _, row in coldspots.iterrows():
            potential = "HIGH" if row['Coldspot_Score'] < 10 else "MEDIUM" if row['Coldspot_Score'] < 20 else "LOW"
            print(f"  {row['Precision Area']:25s}: Score {row['Coldspot_Score']:4.1f} | "
                  f"{row['Sales']/1_000_000:6.3f}M sales, {row['Brand_Competition']:1.0f} brands [{potential}]")
        
        # Geographic clustering analysis
        print(f"\n🗺️ Geographic Clustering Analysis:")
        region_precision = self.df.groupby(['Region', 'Precision Area'])['Sales'].sum().reset_index()
        
        # Find regions with high precision area concentration
        region_precision_count = region_precision.groupby('Region')['Precision Area'].nunique()
        region_precision_sales = region_precision.groupby('Region')['Sales'].sum()
        
        region_precision_metrics = pd.DataFrame({
            'Area_Count': region_precision_count,
            'Total_Sales': region_precision_sales,
            'Sales_Per_Area': region_precision_sales / region_precision_count
        })
        
        print("Regional Precision Area Efficiency:")
        region_precision_metrics_sorted = region_precision_metrics.sort_values('Sales_Per_Area', ascending=False)
        for region, row in region_precision_metrics_sorted.iterrows():
            efficiency = "HIGH" if row['Sales_Per_Area'] > 10000000 else "MEDIUM" if row['Sales_Per_Area'] > 5000000 else "LOW"
            print(f"  {region:20s}: {row['Area_Count']:2.0f} areas, "
                  f"{row['Sales_Per_Area']/1_000_000:6.2f}M avg/area [{efficiency}]")
        
        return {
            'top_hotspot': precision_sales.index[0],
            'top_hotspot_sales': precision_sales_millions.iloc[0],
            'top_coldspot': coldspots.iloc[0]['Precision Area'],
            'most_efficient_region': region_precision_metrics_sorted.index[0]
        }
    
    def seasonal_geographic_patterns(self):
        """Analyze seasonal patterns by geography."""
        print("\n" + "=" * 80)
        print("SEASONAL GEOGRAPHIC PATTERNS")
        print("=" * 80)
        
        # Seasonal analysis by region
        regional_seasonal = self.df.groupby(['Region', 'Season'])['Sales'].sum().reset_index()
        regional_seasonal_pivot = regional_seasonal.pivot(index='Region', columns='Season', values='Sales').fillna(0)
        
        print(f"\n🌡️ Seasonal Performance by Region:")
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
        
        # Ramadan impact analysis by region
        print(f"\n🕌 Ramadan Impact by Region:")
        ramadan_data = self.df.groupby(['Region', 'Ramadan_Period'])['Sales'].sum().reset_index()
        ramadan_pivot = ramadan_data.pivot(index='Region', columns='Ramadan_Period', values='Sales').fillna(0)
        
        ramadan_impact = []
        for region in ramadan_pivot.index:
            ramadan_sales = ramadan_pivot.loc[region, 1] if 1 in ramadan_pivot.columns else 0
            non_ramadan_sales = ramadan_pivot.loc[region, 0] if 0 in ramadan_pivot.columns else 0
            total_months_ramadan = 1
            total_months_non_ramadan = 11
            
            if non_ramadan_sales > 0:
                ramadan_avg = ramadan_sales / total_months_ramadan
                non_ramadan_avg = non_ramadan_sales / total_months_non_ramadan
                impact = (ramadan_avg - non_ramadan_avg) / non_ramadan_avg * 100
                ramadan_impact.append((region, impact))
        
        ramadan_impact.sort(key=lambda x: x[1], reverse=True)
        print("Ramadan Month Impact vs Average:")
        for region, impact in ramadan_impact:
            significance = "HIGH" if impact > 50 else "MODERATE" if impact > 20 else "LOW"
            print(f"  {region:20s}: {impact:+6.1f}% vs average month [{significance}]")
        
        return {
            'ramadan_highest_impact': ramadan_impact[0][0] if ramadan_impact else None,
            'ramadan_highest_impact_pct': ramadan_impact[0][1] if ramadan_impact else 0
        }
    
    def generate_geographic_intelligence(self):
        """Generate comprehensive geographic intelligence report."""
        print("\n" + "=" * 80)
        print("GEOGRAPHIC INTELLIGENCE SUMMARY")
        print("=" * 80)
        
        # Run all analyses
        regional = self.regional_performance_analysis()
        province = self.province_level_deep_dive()
        precision = self.precision_area_hotspot_analysis()
        seasonal = self.seasonal_geographic_patterns()
        
        # Key insights
        print(f"\n🎯 GEOGRAPHIC STRATEGIC INSIGHTS:")
        print(f"• Market Leader Region: {regional['top_region']} ({regional['top_region_share']:.1f}% share)")
        print(f"• Top Expansion Province: {province['top_expansion_province']} (Score: {province['opportunity_score']:.1f})")
        print(f"• Premier Hotspot: {precision['top_hotspot']} ({precision['top_hotspot_sales']:.3f}M sales)")
        
        if seasonal['ramadan_highest_impact']:
            print(f"• Ramadan Sensitivity: {seasonal['ramadan_highest_impact']} "
                  f"({seasonal['ramadan_highest_impact_pct']:+.1f}% impact)")
        
        # Growth opportunities
        if regional['growth_leaders']:
            print(f"\n📈 GROWTH OPPORTUNITIES:")
            print(f"• High-Growth Regions: {', '.join(regional['growth_leaders'][:3])}")
        
        # Risk areas
        if regional['declining_regions']:
            print(f"\n⚠️ AREAS REQUIRING ATTENTION:")
            print(f"• Declining Regions: {', '.join(regional['declining_regions'][:3])}")
        
        # Strategic recommendations
        print(f"\n🚀 GEOGRAPHIC STRATEGIC RECOMMENDATIONS:")
        print(f"1. EXPAND: Prioritize {province['top_expansion_province']} for market development")
        print(f"2. STRENGTHEN: Fortify position in {regional['top_region']} to defend leadership")
        print(f"3. DEVELOP: Target {precision['top_coldspot']} for growth potential")
        
        if seasonal['ramadan_highest_impact_pct'] > 30:
            print(f"4. OPTIMIZE: Implement Ramadan-focused strategies in high-impact regions")
        
        return {
            'primary_focus_region': regional['top_region'],
            'expansion_target': province['top_expansion_province'],
            'growth_potential': len(regional['growth_leaders']),
            'strategic_priority': "HIGH" if len(regional['growth_leaders']) > 3 else "MEDIUM"
        }

def main():
    """Example usage of the geographic analysis module."""
    print("CSD Geographic Analysis Module Ready!")
    print("Use with CSDDatasetLoader to analyze geographic patterns.")

if __name__ == "__main__":
    main()