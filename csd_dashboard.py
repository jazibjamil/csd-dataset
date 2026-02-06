#!/usr/bin/env python3
"""
🥤 Saudi Arabian CSD Market Intelligence Dashboard
Interactive Streamlit Web Application

This dashboard provides real-time insights and interactive visualizations
for the Saudi Arabian Carbonated Soft Drink market analysis.

Run with: streamlit run csd_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import streamlit as st

# Custom CSS to hide the GitHub icon
hide_github_icon = """
<style>
.css-1jc7ptx.e1ewe1squ3, .css-1jc7ptx.e1ewe1squ3.e1ewe1sq0, .css-1jc7ptx.e1ewe1squ3.e1ewe1sq1, .css-1jc7ptx.e1ewe1squ3.e1ewe1sq5, .css-1jc7ptx.e1ewe1squ3.e1ewe1sq4 {
    display: none !important;
}
</style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

# Set page configuration
st.set_page_config(
    page_title="🥤 Saudi CSD Market Intelligence",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #2E86AB;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CSDDashboard:
    """Main dashboard class for CSD market intelligence"""
    
    def __init__(self):
        """Initialize the dashboard"""
        self.df_original = None
        self.df_long = None
        self.load_data()
        
    def load_data(self):
        """Load and prepare the dataset"""
        try:
            # Load original data
            self.df_original = pd.read_excel("DUMMY DATA FOR PRECISION AREAS.xlsx", sheet_name='Sheet6')
            
            # Convert to long format
            monthly_cols = [col for col in self.df_original.columns if "'24" in col]
            id_vars = ['Region', 'Province', 'Precision Area', 'MARKET', 'KEY MANU  & KINZA', 
                      'BRAND', 'Brand-2', 'CSD & CSD +', 'CSD Flavor Segment', 'REG/DIET', 
                      'KEY PACKS', 'SUB-BRAND', 'PACK TYPE', 'PACK SIZE', 'ITEM']
            
            self.df_long = pd.melt(self.df_original, 
                                  id_vars=id_vars,
                                  value_vars=monthly_cols,
                                  var_name='Month',
                                  value_name='Sales')
            
            # Clean and prepare data
            self.df_long['Month'] = self.df_long['Month'].str.replace("'", "")
            self.df_long['Date'] = pd.to_datetime(self.df_long['Month'], format='%b%y')
            self.df_long = self.df_long.sort_values('Date')
            self.df_long['Month_Name'] = self.df_long['Date'].dt.strftime('%B')
            self.df_long['Month_Num'] = self.df_long['Date'].dt.month
            self.df_long['Quarter'] = self.df_long['Date'].dt.quarter
            self.df_long['Sales_Millions'] = self.df_long['Sales'] / 1_000_000
            
            # Add derived features
            self.df_long['Season'] = self.df_long['Month_Num'].map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })
            self.df_long['Ramadan_Period'] = self.df_long['Month_Num'].apply(lambda x: 1 if x == 10 else 0)
            
            st.success("✅ Dataset loaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            st.stop()

    def render_header(self):
        """Render the dashboard header"""
        st.markdown('<h1 class="main-header">🥤 Saudi Arabian CSD Market Intelligence</h1>', 
                   unsafe_allow_html=True)
        
        # Key metrics
        total_sales = self.df_long['Sales'].sum()
        total_millions = total_sales / 1_000_000
        zero_sales_pct = (self.df_long['Sales'] == 0).mean() * 100
        active_markets = self.df_long['MARKET'].nunique()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Market Size", f"{total_millions:.1f}M SAR", "Annual 2024")
        with col2:
            st.metric("🎯 Distribution Coverage", f"{100-zero_sales_pct:.1f}%", "Active markets")
        with col3:
            st.metric("🌍 Active Markets", f"{active_markets}", "Precision areas")
        with col4:
            st.metric("📈 Data Points", f"{len(self.df_long):,}", "Monthly records")

    def render_sidebar(self):
        """Render the sidebar with filters"""
        st.sidebar.header("🔍 Filters & Controls")
        
        # Time period filter
        st.sidebar.subheader("📅 Time Period")
        months = sorted(self.df_long['Month_Name'].unique())
        selected_months = st.sidebar.multiselect(
            "Select Months",
            months,
            default=months
        )
        
        # Region filter
        st.sidebar.subheader("🌍 Geographic Filters")
        regions = sorted(self.df_long['Region'].unique())
        selected_regions = st.sidebar.multiselect(
            "Select Regions",
            regions,
            default=regions
        )
        
        # Manufacturer filter
        st.sidebar.subheader("🏭 Product Filters")
        manufacturers = sorted(self.df_long['KEY MANU  & KINZA'].unique())
        selected_manufacturers = st.sidebar.multiselect(
            "Select Manufacturers",
            manufacturers,
            default=manufacturers
        )
        
        # Pack type filter
        pack_types = sorted(self.df_long['PACK TYPE'].unique())
        selected_pack_types = st.sidebar.multiselect(
            "Select Pack Types",
            pack_types,
            default=pack_types
        )
        
        return selected_months, selected_regions, selected_manufacturers, selected_pack_types

    def apply_filters(self, months, regions, manufacturers, pack_types):
        """Apply filters to the dataset"""
        filtered_df = self.df_long.copy()
        
        if months:
            filtered_df = filtered_df[filtered_df['Month_Name'].isin(months)]
        if regions:
            filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
        if manufacturers:
            filtered_df = filtered_df[filtered_df['KEY MANU  & KINZA'].isin(manufacturers)]
        if pack_types:
            filtered_df = filtered_df[filtered_df['PACK TYPE'].isin(pack_types)]
        
        return filtered_df

    def render_market_overview(self, df):
        """Render market overview section"""
        st.header("📊 Market Overview")
        
        # Monthly sales trend
        monthly_sales = df.groupby('Date')['Sales'].sum().reset_index()
        monthly_sales['Month_Name'] = monthly_sales['Date'].dt.strftime('%B')
        monthly_sales['Sales_Millions'] = monthly_sales['Sales'] / 1_000_000
        
        fig = px.line(monthly_sales, 
                     x='Month_Name', 
                     y='Sales_Millions',
                     title='📈 Monthly Sales Trend',
                     labels={'Month_Name': 'Month', 'Sales_Millions': 'Sales (Millions SAR)'},
                     markers=True,
                     line_shape='spline')
        
        # Add annotations for peak and low months
        peak_month = monthly_sales.loc[monthly_sales['Sales_Millions'].idxmax()]
        low_month = monthly_sales.loc[monthly_sales['Sales_Millions'].idxmin()]
        
        fig.add_annotation(x=peak_month['Month_Name'], y=peak_month['Sales_Millions'],
                          text=f"🔥 Peak: {peak_month['Sales_Millions']:.1f}M",
                          showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                          arrowcolor="red", bgcolor="white", bordercolor="red")
        
        fig.add_annotation(x=low_month['Month_Name'], y=low_month['Sales_Millions'],
                          text=f"❄️ Low: {low_month['Sales_Millions']:.1f}M",
                          showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                          arrowcolor="blue", bgcolor="white", bordercolor="blue")
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Seasonality metrics
        seasonality_ratio = peak_month['Sales'] / low_month['Sales']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Seasonality Ratio", f"{seasonality_ratio:.2f}x", "Peak vs Low month")
        with col2:
            h1_total = monthly_sales[monthly_sales['Date'].dt.month <= 6]['Sales'].sum()
            h2_total = monthly_sales[monthly_sales['Date'].dt.month > 6]['Sales'].sum()
            h2_vs_h1 = ((h2_total - h1_total) / h1_total * 100) if h1_total > 0 else 0
            st.metric("📊 H2 vs H1 Growth", f"{h2_vs_h1:+.1f}%", "Second half stronger")
        with col3:
            cv = monthly_sales['Sales'].std() / monthly_sales['Sales'].mean()
            volatility = "High" if cv > 0.15 else "Moderate" if cv > 0.10 else "Low"
            st.metric("📉 Volatility", f"{cv:.3f} ({volatility})", "Coefficient of variation")

    def render_geographic_analysis(self, df):
        """Render geographic analysis section"""
        st.header("🌍 Geographic Intelligence")
        
        # Regional performance
        regional_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        regional_millions = regional_sales / 1_000_000
        
        fig = px.bar(x=regional_millions.index, 
                     y=regional_millions.values,
                     title='🌍 Regional Sales Performance',
                     labels={'x': 'Region', 'y': 'Sales (Millions SAR)'},
                     text=regional_millions.values.round(1),
                     color=regional_millions.values,
                     color_continuous_scale='viridis')
        
        fig.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Geographic concentration
        regional_shares = regional_sales / regional_sales.sum()
        hhi = (regional_shares ** 2).sum()
        concentration = "High" if hhi > 0.25 else "Moderate" if hhi > 0.15 else "Low"
        
        st.info(f"📊 Market Concentration: {concentration} (HHI: {hhi:.3f})")
        
        # Province analysis
        province_sales = df.groupby('Province')['Sales'].sum().sort_values(ascending=False)
        province_millions = province_sales / 1_000_000
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏆 Top 10 Provinces")
            for i, (province, sales) in enumerate(province_millions.head(10).items(), 1):
                share = (sales / province_sales.sum()) * 100
                st.write(f"{i:2d}. {province}: {sales:.2f}M ({share:.1f}%)")
        
        with col2:
            st.subheader("🎯 Expansion Opportunities")
            # Calculate opportunity scores
            province_metrics = df.groupby('Province').agg({
                'Sales': 'sum',
                'Precision Area': 'nunique',
                'BRAND': 'nunique'
            }).reset_index()
            
            province_metrics['Sales_Per_Area'] = province_metrics['Sales'] / province_metrics['Precision Area']
            province_metrics['Opportunity_Score'] = (
                province_metrics['Sales_Per_Area'].rank(ascending=True) * 0.4 +
                province_metrics['BRAND'].rank(ascending=True) * 0.3 +
                province_metrics['Sales'].rank(ascending=True) * 0.3
            )
            
            top_opportunities = province_metrics.nlargest(5, 'Opportunity_Score')
            for _, row in top_opportunities.iterrows():
                st.write(f"📍 {row['Province']}: Score {row['Opportunity_Score']:.1f}")

    def render_product_analysis(self, df):
        """Render product analysis section"""
        st.header("🥤 Product Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Manufacturer market share
            manu_sales = df.groupby('KEY MANU  & KINZA')['Sales'].sum().sort_values(ascending=False)
            manu_millions = manu_sales / 1_000_000
            total_sales = manu_sales.sum()
            
            fig = px.pie(values=manu_millions.values,
                          names=manu_millions.index,
                          title='🏭 Manufacturer Market Share',
                          labels={'value': 'Sales (Millions SAR)', 'names': 'Manufacturer'})
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Flavor segment analysis
            flavor_sales = df.groupby('CSD Flavor Segment')['Sales'].sum().sort_values(ascending=False)
            flavor_millions = flavor_sales / 1_000_000
            
            fig = px.bar(x=flavor_millions.index, 
                         y=flavor_millions.values,
                         title='🍋 Flavor Segment Preferences',
                         labels={'x': 'Flavor Segment', 'y': 'Sales (Millions SAR)'},
                         color=flavor_millions.values,
                         color_continuous_scale='plasma')
            
            fig.update_traces(texttemplate='%{y:.1f}M', textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Pack type analysis
        pack_type_sales = df.groupby('PACK TYPE')['Sales'].sum().sort_values(ascending=False)
        pack_millions = pack_type_sales / 1_000_000
        
        st.subheader("📦 Pack Type Performance")
        for pack_type, sales in pack_millions.items():
            share = (sales / pack_type_sales.sum()) * 100
            st.write(f"• {pack_type}: {sales:.2f}M ({share:.1f}%)")

    def render_strategic_insights(self, df):
        """Render strategic insights section"""
        st.header("🎯 Strategic Intelligence")
        
        # Distribution gaps analysis
        zero_analysis = df[df['Sales'] == 0].copy()
        total_records = len(df)
        zero_records = len(zero_analysis)
        zero_percentage = (zero_records / total_records) * 100
        
        st.subheader("🚨 Distribution Gap Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Zero Sales Records", f"{zero_records:,}", f"{zero_percentage:.1f}%")
        with col2:
            positive_records = total_records - zero_records
            st.metric("✅ Active Records", f"{positive_records:,}", f"{100-zero_percentage:.1f}%")
        with col3:
            urgency = "🔴 CRITICAL" if zero_percentage > 45 else "🟡 HIGH" if zero_percentage > 35 else "🟢 MODERATE"
            st.metric("⚠️ Priority Level", urgency)
        
        # Geographic distribution gaps
        st.subheader("🌍 Geographic Distribution Gaps")
        zero_by_region = zero_analysis.groupby('Region').size()
        total_by_region = df.groupby('Region').size()
        zero_pct_by_region = (zero_by_region / total_by_region * 100).sort_values(ascending=False)
        
        # Create a dataframe for better display
        gap_df = pd.DataFrame({
            'Region': zero_pct_by_region.index,
            'Zero Sales %': zero_pct_by_region.values,
            'Priority': ['🔴 CRITICAL' if pct > 60 else '🟡 HIGH' if pct > 50 else '🟢 MODERATE' for pct in zero_pct_by_region.values]
        })
        
        st.dataframe(gap_df, use_container_width=True)
        
        # Diet segment opportunity
        st.subheader("🥤 Diet Segment Opportunity")
        
        diet_by_region = df[df['REG/DIET'] == 'DIET'].groupby('Region')['Sales'].sum()
        total_by_region = df.groupby('Region')['Sales'].sum()
        diet_penetration = (diet_by_region / total_by_region * 100).fillna(0).sort_values()
        
        # Create diet opportunity dataframe
        diet_df = pd.DataFrame({
            'Region': diet_penetration.index,
            'Diet Penetration %': diet_penetration.values,
            'Opportunity': ['🔥 HIGH' if pct < 5 else '🟡 MEDIUM' if pct < 10 else '🟢 LOW' for pct in diet_penetration.values]
        })
        
        st.dataframe(diet_df, use_container_width=True)
        
        # Overall diet vs regular
        reg_diet_sales = df.groupby('REG/DIET')['Sales'].sum()
        total_sales = reg_diet_sales.sum()
        diet_share = (reg_diet_sales.get('DIET', 0) / total_sales) * 100
        
        st.info(f"📊 Overall Diet/Regular Split: Regular {reg_diet_sales.get('REG', 0)/1_000_000:.2f}M ({(reg_diet_sales.get('REG', 0)/total_sales)*100:.1f}%) vs Diet {reg_diet_sales.get('DIET', 0)/1_000_000:.2f}M ({diet_share:.1f}%)")
        
        if diet_share < 15:
            st.success("🎯 Diet Market Opportunity: EXTREME - Massive growth potential!")
        elif diet_share < 20:
            st.warning("🎯 Diet Market Opportunity: HIGH - Significant growth opportunity")
        else:
            st.info("🎯 Diet Market Opportunity: MODERATE - Room for improvement")

    def render_interactive_analysis(self, df):
        """Render interactive analysis section"""
        st.header("🔍 Interactive Analysis")
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Cross-Regional Comparison", "Product-Regional Analysis", "Time Series Deep Dive", "Custom Analysis"]
        )
        
        if analysis_type == "Cross-Regional Comparison":
            self.render_cross_regional_analysis(df)
        elif analysis_type == "Product-Regional Analysis":
            self.render_product_regional_analysis(df)
        elif analysis_type == "Time Series Deep Dive":
            self.render_time_series_analysis(df)
        else:
            self.render_custom_analysis(df)

    def render_cross_regional_analysis(self, df):
        """Render cross-regional comparison"""
        st.subheader("🌍 Cross-Regional Performance Comparison")
        
        # Select regions to compare
        regions = sorted(df['Region'].unique())
        selected_regions = st.multiselect("Select regions to compare", regions, default=regions[:3])
        
        if len(selected_regions) >= 2:
            comparison_df = df[df['Region'].isin(selected_regions)]
            
            # Monthly comparison
            monthly_comparison = comparison_df.groupby(['Region', 'Month_Name'])['Sales'].sum().reset_index()
            
            fig = px.line(monthly_comparison, 
                         x='Month_Name', 
                         y='Sales',
                         color='Region',
                         title='📊 Monthly Sales Comparison by Region',
                         labels={'Month_Name': 'Month', 'Sales': 'Sales (SAR)'},
                         markers=True)
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Product mix comparison
            product_comparison = comparison_df.groupby(['Region', 'CSD Flavor Segment'])['Sales'].sum().reset_index()
            
            fig = px.bar(product_comparison, 
                         x='CSD Flavor Segment', 
                         y='Sales',
                         color='Region',
                         title='🍋 Flavor Preferences by Region',
                         labels={'CSD Flavor Segment': 'Flavor', 'Sales': 'Sales (SAR)'},
                         barmode='group')
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

    def render_product_regional_analysis(self, df):
        """Render product-regional analysis"""
        st.subheader("🥤 Product-Regional Analysis")
        
        # Select product category
        product_category = st.selectbox(
            "Select Product Category",
            ["Manufacturer", "Brand", "Flavor Segment", "Pack Type"]
        )
        
        # Select region
        region = st.selectbox("Select Region", sorted(df['Region'].unique()))
        
        # Filter data
        region_df = df[df['Region'] == region]
        
        if product_category == "Manufacturer":
            analysis_data = region_df.groupby('KEY MANU  & KINZA')['Sales'].sum().sort_values(ascending=False)
            title = f"🏭 Manufacturer Performance in {region}"
        elif product_category == "Brand":
            analysis_data = region_df.groupby('BRAND')['Sales'].sum().sort_values(ascending=False)
            title = f"🥤 Brand Performance in {region}"
        elif product_category == "Flavor Segment":
            analysis_data = region_df.groupby('CSD Flavor Segment')['Sales'].sum().sort_values(ascending=False)
            title = f"🍋 Flavor Preferences in {region}"
        else:  # Pack Type
            analysis_data = region_df.groupby('PACK TYPE')['Sales'].sum().sort_values(ascending=False)
            title = f"📦 Pack Type Performance in {region}"
        
        # Create visualization
        analysis_millions = analysis_data / 1_000_000
        
        fig = px.bar(x=analysis_millions.index, 
                     y=analysis_millions.values,
                     title=title,
                     labels={'x': product_category, 'y': 'Sales (Millions SAR)'},
                     color=analysis_millions.values,
                     color_continuous_scale='viridis')
        
        fig.update_traces(texttemplate='%{y:.1f}M', textposition='outside')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table
        st.subheader("📊 Detailed Breakdown")
        display_df = pd.DataFrame({
            product_category: analysis_data.index,
            'Sales (Millions SAR)': analysis_millions.values,
            'Market Share (%)': (analysis_data / analysis_data.sum() * 100).values
        })
        st.dataframe(display_df, use_container_width=True)

    def render_time_series_analysis(self, df):
        """Render time series deep dive"""
        st.subheader("📈 Time Series Deep Dive")
        
        # Select analysis dimension
        ts_dimension = st.selectbox(
            "Select Time Series Dimension",
            ["Overall Market", "By Region", "By Manufacturer", "By Product"]
        )
        
        if ts_dimension == "Overall Market":
            ts_data = df.groupby('Date')['Sales'].sum().reset_index()
            title = "📊 Overall Market Time Series"
        elif ts_dimension == "By Region":
            region = st.selectbox("Select Region", sorted(df['Region'].unique()))
            ts_data = df[df['Region'] == region].groupby('Date')['Sales'].sum().reset_index()
            title = f"📊 {region} Time Series"
        elif ts_dimension == "By Manufacturer":
            manufacturer = st.selectbox("Select Manufacturer", sorted(df['KEY MANU  & KINZA'].unique()))
            ts_data = df[df['KEY MANU  & KINZA'] == manufacturer].groupby('Date')['Sales'].sum().reset_index()
            title = f"📊 {manufacturer} Time Series"
        else:  # By Product
            product = st.selectbox("Select Product", sorted(df['BRAND'].unique())[:20])  # Limit to first 20
            ts_data = df[df['BRAND'] == product].groupby('Date')['Sales'].sum().reset_index()
            title = f"📊 {product} Time Series"
        
        # Create time series plot
        ts_data['Sales_Millions'] = ts_data['Sales'] / 1_000_000
        
        fig = px.line(ts_data, 
                     x='Date', 
                     y='Sales_Millions',
                     title=title,
                     labels={'Date': 'Date', 'Sales_Millions': 'Sales (Millions SAR)'},
                     markers=True)
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add trend analysis
        st.subheader("📊 Trend Analysis")
        
        # Calculate growth rates
        ts_data['Growth_Rate'] = ts_data['Sales'].pct_change() * 100
        avg_growth = ts_data['Growth_Rate'].mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Average Growth Rate", f"{avg_growth:+.2f}%", "Month-over-month")
        with col2:
            volatility = ts_data['Sales'].std() / ts_data['Sales'].mean()
            st.metric("📉 Volatility", f"{volatility:.3f}", "Coefficient of variation")
        with col3:
            max_sales = ts_data['Sales_Millions'].max()
            min_sales = ts_data['Sales_Millions'].min()
            st.metric("📊 Range", f"{min_sales:.1f}M - {max_sales:.1f}M", "Min to Max")

    def render_custom_analysis(self, df):
        """Render custom analysis"""
        st.subheader("🔧 Custom Analysis")
        
        # Select dimensions for analysis
        col1, col2 = st.columns(2)
        with col1:
            dimension1 = st.selectbox("First Dimension", 
                                    ['Region', 'Province', 'Manufacturer', 'Brand', 'Flavor', 'Pack Type'])
        with col2:
            dimension2 = st.selectbox("Second Dimension", 
                                    ['Region', 'Province', 'Manufacturer', 'Brand', 'Flavor', 'Pack Type'])
        
        if dimension1 != dimension2:
            # Create cross-tabulation analysis
            cross_tab = df.groupby([dimension1, dimension2])['Sales'].sum().reset_index()
            
            # Create heatmap
            pivot_data = cross_tab.pivot(index=dimension1, columns=dimension2, values='Sales')
            pivot_data_millions = pivot_data / 1_000_000
            
            fig = px.imshow(pivot_data_millions, 
                           title=f"🔥 {dimension1} vs {dimension2} Heatmap",
                           labels=dict(x=dimension2, y=dimension1, color="Sales (Millions SAR)"),
                           color_continuous_scale='viridis')
            
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show top combinations
            st.subheader("🏆 Top Combinations")
            top_combinations = cross_tab.nlargest(10, 'Sales')
            top_combinations['Sales (Millions)'] = top_combinations['Sales'] / 1_000_000
            st.dataframe(top_combinations, use_container_width=True)

    def render_export_section(self, df):
        """Render data export section"""
        st.header("📤 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Download Analysis Results")
            
            # Prepare data for export
            export_df = df.copy()
            export_df['Sales_Millions'] = export_df['Sales'] / 1_000_000
            
            # Create download button
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='csd_analysis_results.csv',
                mime='text/csv'
            )
        
        with col2:
            st.subheader("📈 Summary Statistics")
            
            # Calculate summary statistics
            summary_stats = {
                'Total Sales (Millions SAR)': df['Sales_Millions'].sum(),
                'Average Sales (SAR)': df['Sales'].mean(),
                'Median Sales (SAR)': df['Sales'].median(),
                'Max Sales (SAR)': df['Sales'].max(),
                'Min Sales (SAR)': df['Sales'].min(),
                'Total Records': len(df),
                'Zero Sales Records': (df['Sales'] == 0).sum(),
                'Active Markets': df['MARKET'].nunique(),
                'Unique Brands': df['BRAND'].nunique()
            }
            
            stats_df = pd.DataFrame(list(summary_stats.items()), 
                                  columns=['Metric', 'Value'])
            st.dataframe(stats_df, use_container_width=True)

    def run(self):
        """Main dashboard execution"""
        # Render header
        self.render_header()
        
        # Get filters
        months, regions, manufacturers, pack_types = self.render_sidebar()
        
        # Apply filters
        filtered_df = self.apply_filters(months, regions, manufacturers, pack_types)
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Market Overview", 
            "🌍 Geographic Analysis", 
            "🥤 Product Analysis",
            "🎯 Strategic Insights",
            "🔍 Interactive Analysis",
            "📤 Export Data"
        ])
        
        with tab1:
            self.render_market_overview(filtered_df)
        
        with tab2:
            self.render_geographic_analysis(filtered_df)
        
        with tab3:
            self.render_product_analysis(filtered_df)
        
        with tab4:
            self.render_strategic_insights(filtered_df)
        
        with tab5:
            self.render_interactive_analysis(filtered_df)
        
        with tab6:
            self.render_export_section(filtered_df)
        
        # Footer
        st.markdown("---")
        st.markdown("🥤 **Saudi Arabian CSD Market Intelligence Dashboard**")
        st.markdown("Built with Streamlit • Real-time Interactive Analytics")
        st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main execution
if __name__ == "__main__":
    dashboard = CSDDashboard()
    dashboard.run()