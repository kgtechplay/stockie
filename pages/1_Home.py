import streamlit as st
import pandas as pd
import sys
import os
from difflib import SequenceMatcher

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from supabase_connect import supabase_anon
    from utils.config import setup_page_config
    from utils.auth import check_environment_variables
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure page
setup_page_config()

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_ticker_fuzzy(company_name):
    """
    Fuzzy search for company tickers
    Returns top 5 matches based on similarity
    """
    if len(company_name) < 3:
        return []
    
    ticker = []
    n = 5
    search_name = "%" + company_name + "%"
    
    try:
        # Fuzzy search using case-insensitive partial match
        value = supabase_anon.table("Company_ticker_all").select("*").ilike("name", search_name).execute()
        
        if not value.data:
            return []
        
        # Sort results by string similarity
        sorted_matches = sorted(
            value.data,
            key=lambda row: similarity(company_name, row["name"]),
            reverse=True
        )
        
        # Get top n matches
        top_matches = sorted_matches[:n]
        
        for row in top_matches:
            ticker.append({
                'cik': row['cik'],
                'ticker': row['ticker'], 
                'exchange': row['exchange'],
                'name': row['name'],
                'display': f"{row['ticker']} - {row['name']} ({row['exchange']})"
            })
        
        return ticker
        
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

# Check environment variables
env_check = check_environment_variables()
if not env_check['all_set']:
    st.error("⚠️ Environment variables not configured. Please check your .env file.")
    st.stop()

# Main page content
def main():
    # Display banner if it exists
    banner_path = "assets/images/stockie-banner.png"
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        # Fallback banner
        st.markdown("""
        <div style='text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0; font-size: 3rem;'>📈 STOCKIE</h1>
            <p style='color: white; margin: 0; font-size: 1.2rem;'>Your Ultimate Stock Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search section
    st.markdown("### 🔍 Search for Stock Name")
    
    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'selected_stock' not in st.session_state:
        st.session_state.selected_stock = None
    
    # Search input
    search_input = st.text_input(
        "Enter company name or ticker (minimum 3 characters)",
        value=st.session_state.search_query,
        placeholder="e.g., Apple, AAPL, Microsoft...",
        key="search_box"
    )
    
    # Update search when input changes
    if search_input != st.session_state.search_query:
        st.session_state.search_query = search_input
        if len(search_input) >= 3:
            with st.spinner("Searching..."):
                st.session_state.search_results = get_ticker_fuzzy(search_input)
        else:
            st.session_state.search_results = []
        st.session_state.selected_stock = None
    
    # Display search results in dropdown
    if st.session_state.search_results:
        st.markdown("**📋 Search Results:**")
        
        # Create options for selectbox
        options = ["Select a company..."] + [result['display'] for result in st.session_state.search_results]
        
        selected_option = st.selectbox(
            "Choose from the results:",
            options,
            key="stock_selector"
        )
        
        # Handle selection
        if selected_option != "Select a company...":
            # Find the selected stock data
            for result in st.session_state.search_results:
                if result['display'] == selected_option:
                    st.session_state.selected_stock = result
                    break
    
    # Display selected stock information
    if st.session_state.selected_stock:
        st.markdown("---")
        st.markdown("### 📊 Selected Stock Information")
        
        stock = st.session_state.selected_stock
        
        # Display stock details in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Ticker", stock['ticker'])
        
        with col2:
            st.metric("Exchange", stock['exchange'])
        
        with col3:
            st.metric("CIK", stock['cik'])
        
        with col4:
            st.metric("Status", "✅ Active")
        
        # Company name
        st.markdown(f"**Company Name:** {stock['name']}")
        
        # Action buttons
        st.markdown("### 🛠️ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 View Analytics", type="primary"):
                st.success(f"Redirecting to analytics for {stock['ticker']}...")
        
        with col2:
            if st.button("📥 Import Data"):
                st.info(f"Starting data import for {stock['ticker']}...")
        
        with col3:
            if st.button("📋 Add to Watchlist"):
                st.success(f"Added {stock['ticker']} to your watchlist!")
    
    elif len(st.session_state.search_query) >= 3 and not st.session_state.search_results:
        st.warning(f"No results found for '{st.session_state.search_query}'. Try a different search term.")
    
    elif len(st.session_state.search_query) > 0 and len(st.session_state.search_query) < 3:
        st.info("💡 Enter at least 3 characters to start searching")
    
    # Welcome content when no search
    if not st.session_state.search_query:
        st.markdown("---")
        st.markdown("""
        ### 👋 Welcome to Stockie!
        
        **Get started by searching for a stock above.** Here's what you can do:
        
        **🔍 Smart Search Features:**
        - Search by company name (e.g., "Apple", "Microsoft")
        - Search by ticker symbol (e.g., "AAPL", "MSFT") 
        - Fuzzy matching finds similar companies
        - Real-time results as you type
        
        **📊 What's Available:**
        - Comprehensive stock database
        - Real-time price data
        - Historical analysis
        - Interactive charts
        - Portfolio tracking
        
        **🚀 Popular Searches:**
        """)
        
        # Popular stocks as clickable buttons
        popular_stocks = ["Apple", "Microsoft", "Google", "Amazon", "Tesla"]
        
        cols = st.columns(len(popular_stocks))
        for i, stock in enumerate(popular_stocks):
            with cols[i]:
                if st.button(f"🔍 {stock}", key=f"popular_{stock}"):
                    st.session_state.search_query = stock
                    st.rerun()

if __name__ == "__main__":
    main()
