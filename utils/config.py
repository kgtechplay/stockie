"""
Configuration utilities for Streamlit app
"""

import streamlit as st

def setup_page_config():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Stockie - Stock Analysis",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/kgtechplay/stockie',
            'Report a bug': 'https://github.com/kgtechplay/stockie/issues',
            'About': """
            # Stockie Stock Analysis Dashboard
            
            A comprehensive stock analysis tool built with Streamlit.
            
            **Features:**
            - Real-time stock data
            - Interactive charts
            - Company analysis
            - Portfolio tracking
            
            Built with ❤️ using Python & Streamlit
            """
        }
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        .stMetric {
            background-color: #f0f2f6;
            border-radius: 0.5rem;
            padding: 1rem;
            border-left: 4px solid #1f77b4;
        }
        
        .css-1d391kg {
            padding-top: 1rem;
        }
        
        .stAlert {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

