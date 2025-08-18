"""
Stock Dashboard - Main analytics page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import setup_page_config
from utils.auth import check_environment_variables

# Configure page
setup_page_config()

# Check environment
env_check = check_environment_variables()
if not env_check['all_set']:
    st.error("⚠️ Environment variables not configured. Please check the main app page.")
    st.stop()

st.title("📊 Stock Analytics Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("📋 Filters")
selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    options=["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"],
    default=["AAPL", "GOOGL"]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    max_value=datetime.now()
)

# Main content
if selected_stocks:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Price Charts", "📊 Analytics", "📋 Data Table"])
    
    with tab1:
        st.subheader("Stock Price Trends")
        
        # Sample data for demonstration
        dates = pd.date_range(start=date_range[0], end=date_range[1], freq='D')
        
        fig = go.Figure()
        
        for stock in selected_stocks:
            # Generate sample data (replace with actual data from your database)
            import numpy as np
            np.random.seed(42)
            prices = 100 + np.cumsum(np.random.randn(len(dates)) * 2)
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=prices,
                mode='lines',
                name=stock,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="Stock Price Comparison",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Stock Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Volume analysis
            volume_data = pd.DataFrame({
                'Stock': selected_stocks,
                'Avg Volume': [1500000, 2000000, 1800000, 2200000, 1700000][:len(selected_stocks)]
            })
            
            fig_volume = px.bar(
                volume_data, 
                x='Stock', 
                y='Avg Volume',
                title="Average Trading Volume",
                color='Stock'
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col2:
            # Performance metrics
            performance_data = pd.DataFrame({
                'Stock': selected_stocks,
                'Performance': [5.2, -2.1, 3.8, 8.5, 1.2][:len(selected_stocks)]
            })
            
            fig_perf = px.bar(
                performance_data,
                x='Stock',
                y='Performance',
                title="Performance (%)",
                color='Performance',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_perf, use_container_width=True)
    
    with tab3:
        st.subheader("Stock Data Summary")
        
        # Sample data table
        summary_data = pd.DataFrame({
            'Stock': selected_stocks,
            'Current Price': [150.25, 2800.50, 310.75, 245.80, 3200.25][:len(selected_stocks)],
            'Change': ['+2.5%', '-1.2%', '+0.8%', '+3.2%', '-0.5%'][:len(selected_stocks)],
            'Volume': ['1.5M', '2.0M', '1.8M', '2.2M', '1.7M'][:len(selected_stocks)],
            'Market Cap': ['2.4T', '1.8T', '2.3T', '800B', '1.5T'][:len(selected_stocks)]
        })
        
        st.dataframe(summary_data, use_container_width=True)
        
        # Download button
        csv = summary_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"stock_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Please select at least one stock from the sidebar to view analytics.")

# Footer
st.markdown("---")
st.markdown("*Data is refreshed every 15 minutes during market hours*")
