#!/usr/bin/env python3
"""
Strategic Insights Analysis Module
Saudi Arabian CSD Dataset Analysis Pipeline

This module provides advanced strategic intelligence and competitive analysis.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class CSDStrategicAnalysis:
    """Advanced strategic analysis for competitive intelligence."""
    
    def __init__(self, df_long):
        """
        Initialize with long format dataset.
        
        Args:
            df_long (pd.DataFrame): Long format dataset
        """
        self.df = df_long.copy()
        
    def analyze_distribution_gaps(self):
        """Analyze distribution gaps and inefficiencies."""
        print("=" * 80)
        print("DISTRIBUTION GAP ANALYSIS")
        print("=" * 80)
        
        zero_analysis = self.df[self.df['Sales'] == 0].copy()
        total_records = len(self.df)
        zero_records = len(zero_analysis)
        
        print(f"\n📊 Overall Distribution Gap Analysis:")
        print(f"• Zero Sales Records: {zero_records:,} ({zero_records/total_records*100:.1f}%)")
        print(f"• Positive Sales Records: {total_records-zero_records:,} ({(1-zero_records/total_records)*100:.1f}%)")
        
        # Geographic distribution gaps
        print(f"\n🌍 Geographic Distribution Gaps:")
        zero_by_region = zero_analysis.groupby('Region').size()
        total_by_region = self.df.groupby('Region').size()
        zero_pct_by_region = (zero_by_region / total_by_region * 100).sort_values(ascending=False)
        
        print("Top 5 Regions with Highest Zero Sales %:")
        for region, pct in zero_pct_by_region.head(5).items():
            print(f"  {region:20s}: {pct:.1f}% zero sales")
        
        # Manufacturer-specific gaps
        print(f"\n🏭 Manufacturer Distribution Gaps:")
        zero_by_manu = zero_analysis.groupby('KEY MANU  & KINZA').size()
        total_by_manu = self.df.groupby('KEY MANU  & KINZA').size()
        zero_pct_by_manu = (zero_by_manu / total_by_manu * 100).sort_values(ascending=False)
        
        for manu, pct in zero_pct_by_manu.items():
            print(f"  {manu:20s}: {pct:.1f}% zero sales")
        
        # Pack type inefficiencies
        print(f"\n📦 Pack Type Distribution Inefficiencies:")
        zero_by_pack = zero_analysis.groupby('PACK TYPE').size()
        total_by_pack = self.df.groupby('PACK TYPE').size()
        zero_pct_by_pack = (zero_by_pack / total_by_pack * 100).sort_values(ascending=False)
        
        for pack_type, pct in zero_pct_by_pack.items():
            status = "CRITICAL" if pct > 60 else "HIGH" if pct > 40 else "MODERATE"
            print(f"  {pack_type:15s}: {pct:.1f}% zero sales [{status}]")
        
        return {
            'overall_gap_pct': zero_records/total_records*100,
            'worst_region': zero_pct_by_region.index[0],
            'worst_region_pct': zero_pct_by_region.iloc[0],
            'worst_pack_type': zero_pct_by_pack.index[0],
            'worst_pack_type_pct': zero_pct_by_pack.iloc[0]
        }
    
    def analyze_white_space_opportunities(self):
        """Identify white space opportunities in the market."""
        print("\n" + "=" * 80)
        print("WHITE SPACE OPPORTUNITY ANALYSIS")
        print("=" * 80)
        
        # Diet segment penetration
        print(f"\n🥤 Diet Segment Penetration Analysis:")
        diet_by_region = self.df[self.df['REG/DIET'] == 'DIET'].groupby('Region')['Sales'].sum()
        total_by_region = self.df.groupby('Region')['Sales'].sum()
        diet_penetration = (diet_by_region / total_by_region * 100).fillna(0).sort_values()
        
        print("Regions with Lowest Diet Penetration (Opportunity Areas):")
        for region, penetration in diet_penetration.head(3).items():
            opportunity = "HIGH" if penetration < 5 else "MODERATE" if penetration < 10 else "LOW"
            print(f"  {region:20s}: {penetration:.1f}% diet penetration [{opportunity}]")
        
        # Flavor segment gaps
        print(f"\n🍋 Flavor Segment Gap Analysis:")
        major_flavors = ['COLA', 'CITRUS', 'MANGO', 'ORANGE']
        flavor_opportunities = {}
        
        for flavor in major_flavors:
            gaps = []
            for region in self.df['Region'].unique():
                flavor_sales = self.df[(self.df['Region'] == region) & 
                                      (self.df['CSD Flavor Segment'] == flavor)]['Sales'].sum()
                region_total = self.df[self.df['Region'] == region]['Sales'].sum()
                share = (flavor_sales / region_total * 100) if region_total > 0 else 0
                if share < 5 and region_total > 0:
                    gaps.append(region)
            flavor_opportunities[flavor] = gaps
            print(f"  {flavor:10s}: {len(gaps)} regions with <5% penetration")
        
        # Geographic expansion opportunities
        print(f"\n🌏 Geographic Expansion Opportunity Scoring:")
        province_metrics = self.df.groupby('Province').agg({
            'Sales': 'sum',
            'Precision Area': 'nunique',
            'BRAND': 'nunique'
        }).reset_index()
        
        province_metrics['Sales_Per_Area'] = province_metrics['Sales'] / province_metrics['Precision Area']
        province_metrics['Brand_Density'] = province_metrics['BRAND'] / province_metrics['Precision Area']
        
        # Opportunity score (inverse of current performance)
        province_metrics['Opportunity_Score'] = (
            province_metrics['Sales_Per_Area'].rank(ascending=True) * 0.4 +
            province_metrics['Brand_Density'].rank(ascending=True) * 0.3 +
            province_metrics['Sales'].rank(ascending=True) * 0.3
        )
        
        top_opportunities = province_metrics.nlargest(5, 'Opportunity_Score')
        print("Top 5 Provinces for Expansion:")
        for _, row in top_opportunities.iterrows():
            print(f"  {row['Province']:20s}: Score {row['Opportunity_Score']:.1f} | "
                  f"{row['Sales']/1_000_000:.1f}M sales, {row['Precision Area']} areas")
        
        return {
            'lowest_diet_penetration_region': diet_penetration.index[0],
            'lowest_diet_penetration_pct': diet_penetration.iloc[0],
            'top_expansion_province': top_opportunities.iloc[0]['Province'],
            'expansion_opportunity_score': top_opportunities.iloc[0]['Opportunity_Score']
        }
    
    def analyze_competitive_vulnerabilities(self):
        """Identify competitive vulnerabilities and market concentration risks."""
        print("\n" + "=" * 80)
        print("COMPETITIVE VULNERABILITY ANALYSIS")
        print("=" * 80)
        
        # Manufacturer concentration risk
        print(f"\n🏆 Manufacturer Concentration Risk Analysis:")
        manu_region = self.df.groupby(['Region', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
        region_totals = manu_region.groupby('Region')['Sales'].sum()
        vulnerabilities = []
        
        for region in self.df['Region'].unique():
            region_manu = manu_region[manu_region['Region'] == region]
            region_total = region_totals[region]
            region_manu['Share'] = region_manu['Sales'] / region_total * 100
            
            # Check for high concentration
            top_share = region_manu['Share'].max()
            if top_share > 70:
                top_manu = region_manu.loc[region_manu['Share'].idxmax(), 'KEY MANU  & KINZA']
                risk_level = "CRITICAL" if top_share > 80 else "HIGH"
                vulnerabilities.append((region, top_manu, top_share, risk_level))
        
        if vulnerabilities:
            print("High Concentration Risks (>70% market share):")
            for region, manu, share, risk in sorted(vulnerabilities, key=lambda x: x[2], reverse=True):
                print(f"  {region:20s}: {manu:15s} dominates with {share:.1f}% [{risk}]")
        else:
            print("✅ No critical concentration risks identified")
        
        # Market share erosion warnings
        print(f"\n📉 Market Share Erosion Early Warning:")
        manu_monthly = self.df.groupby(['Month_Num', 'KEY MANU  & KINZA'])['Sales'].sum().reset_index()
        total_monthly_sales = self.df.groupby('Month_Num')['Sales'].sum()
        manu_monthly['Market_Share'] = manu_monthly.apply(
            lambda x: x['Sales'] / total_monthly_sales.loc[x['Month_Num']] * 100, axis=1
        )
        
        warnings_list = []
        for manu in self.df['KEY MANU  & KINZA'].unique():
            manu_data = manu_monthly[manu_monthly['KEY MANU  & KINZA'] == manu].sort_values('Month_Num')
            if len(manu_data) >= 6:
                recent_share = manu_data.tail(3)['Market_Share'].mean()
                peak_share = manu_data['Market_Share'].max()
                if recent_share < peak_share * 0.9:  # 10% decline from peak
                    decline_pct = peak_share - recent_share
                    urgency = "URGENT" if decline_pct > 3 else "MONITOR"
                    warnings_list.append((manu, decline_pct, urgency))
        
        if warnings_list:
            print("Market Share Erosion Warnings:")
            for manu, decline, urgency in sorted(warnings_list, key=lambda x: x[1], reverse=True):
                print(f"  {manu:15s}: {decline:.1f}% share decline from peak [{urgency}]")
        else:
            print("✅ No significant market share erosion detected")
        
        return {
            'concentration_vulnerabilities': len(vulnerabilities),
            'erosion_warnings': len(warnings_list),
            'most_vulnerable_region': vulnerabilities[0][0] if vulnerabilities else None
        }
    
    def analyze_emerging_trends(self):
        """Identify emerging trends and growth patterns."""
        print("\n" + "=" * 80)
        print("EMERGING TRENDS ANALYSIS")
        print("=" * 80)
        
        # Pack type evolution
        print(f"\n📦 Emerging Package Trends:")
        pack_monthly = self.df.groupby(['Month_Num', 'PACK TYPE'])['Sales'].sum().reset_index()
        pack_pivot = pack_monthly.pivot(index='Month_Num', columns='PACK TYPE', values='Sales').fillna(0)
        
        # Calculate growth rates
        pack_growth = {}
        for pack_type in pack_pivot.columns:
            if pack_pivot[pack_type].iloc[0] > 0:
                growth = (pack_pivot[pack_type].iloc[-1] - pack_pivot[pack_type].iloc[0]) / pack_pivot[pack_type].iloc[0] * 100
                pack_growth[pack_type] = growth
        
        print("Package Type Growth (Jan vs Dec):")
        for pack_type, growth in sorted(pack_growth.items(), key=lambda x: x[1], reverse=True):
            trend = "EXPLOSIVE" if growth > 50 else "STRONG" if growth > 20 else "MODERATE" if growth > 0 else "DECLINING"
            print(f"  {pack_type:15s}: {growth:+6.1f}% [{trend}]")
        
        # Regional growth patterns
        print(f"\n🌍 Regional Growth Patterns:")
        regional_growth = self.df.groupby(['Month_Num', 'Region'])['Sales'].sum().reset_index()
        growth_regions = []
        
        for region in self.df['Region'].unique():
            region_data = regional_growth[regional_growth['Region'] == region].sort_values('Month_Num')
            if len(region_data) >= 6:
                recent_avg = region_data.tail(3)['Sales'].mean()
                early_avg = region_data.head(3)['Sales'].mean()
                if recent_avg > early_avg * 1.3:  # 30% growth
                    growth_factor = recent_avg / early_avg
                    growth_regions.append((region, growth_factor))
        
        if growth_regions:
            print("High-Growth Regions (Leading Indicators):")
            for region, growth in sorted(growth_regions, key=lambda x: x[1], reverse=True):
                momentum = "EXPLOSIVE" if growth > 2.0 else "STRONG" if growth > 1.5 else "MODERATE"
                print(f"  {region:20s}: {growth:.2f}x growth rate [{momentum}]")
        else:
            print("No regions showing >30% growth pattern")
        
        # Flavor growth catalysts
        print(f"\n🍋 Flavor Growth Catalysts:")
        flavor_region_growth = self.df.groupby(['Region', 'CSD Flavor Segment', 'Month_Num'])['Sales'].sum().reset_index()
        catalysts = []
        
        for region in self.df['Region'].unique():
            region_data = flavor_region_growth[flavor_region_growth['Region'] == region]
            for flavor in region_data['CSD Flavor Segment'].unique():
                flavor_data = region_data[region_data['CSD Flavor Segment'] == flavor].sort_values('Month_Num')
                if len(flavor_data) >= 6:
                    recent_avg = flavor_data.tail(3)['Sales'].mean()
                    early_avg = flavor_data.head(3)['Sales'].mean()
                    if recent_avg > early_avg * 1.5 and early_avg > 0:  # 50% growth
                        catalysts.append((region, flavor, recent_avg/early_avg))
        
        if catalysts:
            print("Regional Growth Catalysts:")
            for region, flavor, growth in sorted(catalysts, key=lambda x: x[2], reverse=True)[:5]:
                print(f"  {region:20s} - {flavor:10s}: {growth:.2f}x growth")
        else:
            print("No significant flavor growth catalysts identified")
        
        return {
            'top_emerging_pack': max(pack_growth, key=pack_growth.get) if pack_growth else None,
            'top_pack_growth': max(pack_growth.values()) if pack_growth else 0,
            'growth_regions': len(growth_regions),
            'growth_catalysts': len(catalysts)
        }
    
    def generate_strategic_recommendations(self):
        """Generate actionable strategic recommendations."""
        print("\n" + "=" * 80)
        print("STRATEGIC RECOMMENDATIONS")
        print("=" * 80)
        
        # Run all analyses
        distribution_gaps = self.analyze_distribution_gaps()
        white_space = self.analyze_white_space_opportunities()
        competitive = self.analyze_competitive_vulnerabilities()
        trends = self.analyze_emerging_trends()
        
        print(f"\n🚀 IMMEDIATE ACTIONS (0-3 months):")
        if distribution_gaps['overall_gap_pct'] > 40:
            print(f"🔥 CRITICAL: Fix {distribution_gaps['overall_gap_pct']:.1f}% distribution gaps - "
                  f"Target {distribution_gaps['worst_pack_type']} pack type with "
                  f"{distribution_gaps['worst_pack_type_pct']:.1f}% failure rate")
        
        if white_space['lowest_diet_penetration_pct'] < 10:
            print(f"🥤 LAUNCH: Diet segment expansion in {white_space['lowest_diet_penetration_region']} "
                  f"({white_space['lowest_diet_penetration_pct']:.1f}% penetration)")
        
        if trends['top_pack_growth'] > 20:
            print(f"📦 SCALE: Emerging pack type '{trends['top_emerging_pack']}' showing "
                  f"{trends['top_pack_growth']:.1f}% growth")
        
        print(f"\n📈 MEDIUM-TERM STRATEGIES (3-12 months):")
        if competitive['concentration_vulnerabilities'] > 3:
            print(f"🎯 ATTACK: Exploit {competitive['concentration_vulnerabilities']} regions with "
                  f"high manufacturer concentration")
        
        if white_space['expansion_opportunity_score'] > 20:
            print(f"🌏 EXPAND: Geographic expansion into {white_space['top_expansion_province']} "
                  f"(Opportunity Score: {white_space['expansion_opportunity_score']:.1f})")
        
        if competitive['erosion_warnings'] > 0:
            print(f"⚡ CAPITALIZE: {competitive['erosion_warnings']} competitors showing market share erosion")
        
        print(f"\n🎖️ LONG-TERM INITIATIVES (12+ months):")
        print(f"🔬 OPTIMIZE: Data-driven portfolio management based on seasonal patterns")
        print(f"🛡️ DEFEND: Build market intelligence system for competitive monitoring")
        print(f"📊 PREDICT: Advanced analytics for market forecasting and trend prediction")
        
        # ROI Summary
        estimated_immediate_roi = (distribution_gaps['overall_gap_pct'] * 0.15 +  # Distribution fixes
                                 (10 - white_space['lowest_diet_penetration_pct']) * 0.2 +  # Diet expansion
                                 trends['top_pack_growth'] * 0.05)  # Emerging trends
        
        print(f"\n💰 ESTIMATED IMPACT:")
        print(f"• Immediate Revenue Uplift: {estimated_immediate_roi:.1f}%")
        print(f"• 12-Month Strategic ROI: {estimated_immediate_roi * 2:.1f}%")
        print(f"• Long-term Competitive Advantage: HIGH")
        
        return {
            'immediate_actions': 3,
            'medium_term_strategies': 3,
            'estimated_immediate_roi': estimated_immediate_roi,
            'strategic_priority': "HIGH" if distribution_gaps['overall_gap_pct'] > 45 else "MEDIUM"
        }

def main():
    """Example usage of the strategic analysis module."""
    print("CSD Strategic Analysis Module Ready!")
    print("Use with CSDDatasetLoader to analyze competitive intelligence.")

if __name__ == "__main__":
    main()