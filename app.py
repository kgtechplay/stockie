"""
Stockie - Stock Analysis Dashboard
Main Streamlit Application Entry Point
"""

import streamlit as st
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
from utils.config import setup_page_config
from utils.auth import check_environment_variables

def main():
    """Main application entry point"""
    
    # Configure the Streamlit page
    setup_page_config()
    
    # Check if environment variables are properly configured
    env_check = check_environment_variables()
    
    if not env_check['all_set']:
        st.error("⚠️ Environment Configuration Required")
        st.markdown("Please configure the following environment variables in your `.env` file:")
        
        for var, status in env_check['missing'].items():
            if not status:
                st.markdown(f"- `{var}`")
        
        st.markdown("---")
        st.markdown("### 📋 Setup Instructions:")
        st.markdown("""
        1. Copy the `.env` file template in your project root
        2. Add your actual API keys and database credentials
        3. Restart the Streamlit app
        """)
        st.stop()
    
    # Main app content
    st.title("📈 Stockie - Stock Analysis Dashboard")
    st.markdown("---")
    
    # Sidebar navigation info
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    Use the pages in the sidebar to:
    - **📊 Dashboard**: View stock analytics
    - **🔍 Stock Search**: Find and analyze stocks
    - **📋 Data Import**: Import new stock data
    - **⚙️ Settings**: Configure the application
    """)
    
    # Main dashboard content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Available Stocks",
            value="Loading...",
            delta="",
            help="Total number of stocks in database"
        )
    
    with col2:
        st.metric(
            label="Last Updated",
            value="Loading...",
            delta="",
            help="Last time stock data was refreshed"
        )
    
    with col3:
        st.metric(
            label="Status",
            value="✅ Online",
            delta="",
            help="System status"
        )
    
    st.markdown("---")
    
    # Welcome content
    st.markdown("""
    ### Welcome to Stockie! 👋
    
    This is your comprehensive stock analysis dashboard. Here's what you can do:
    
    **📊 Key Features:**
    - Real-time stock data analysis
    - Historical trend visualization
    - Company information lookup
    - Portfolio tracking
    - Data import and management
    
    **🚀 Getting Started:**
    1. Use the **Stock Search** page to find companies
    2. View detailed analytics on the **Dashboard**
    3. Import new data using the **Data Import** page
    4. Customize settings in the **Settings** page
    
    Select a page from the sidebar to begin exploring!
    """)

if __name__ == "__main__":
    main()

