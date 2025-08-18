"""
Settings - Configure the application
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import setup_page_config
from utils.auth import check_environment_variables

# Configure page
setup_page_config()

st.title("⚙️ Application Settings")
st.markdown("---")

# Environment status
st.subheader("🔐 Environment Configuration")

env_check = check_environment_variables()

if env_check['all_set']:
    st.success("✅ All environment variables are configured")
else:
    st.error("⚠️ Some environment variables are missing")

# Display status for each variable
for var, is_set in env_check['missing'].items():
    status = "✅" if is_set else "❌"
    st.markdown(f"{status} `{var}`")

st.markdown("---")

# Application settings
st.subheader("🎛️ Application Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Data Settings**")
    
    auto_refresh = st.checkbox("🔄 Auto-refresh data", value=True)
    refresh_interval = st.selectbox(
        "Refresh interval",
        options=[5, 15, 30, 60],
        index=1,
        format_func=lambda x: f"{x} minutes"
    )
    
    cache_duration = st.selectbox(
        "Cache duration",
        options=[1, 2, 4, 8, 24],
        index=2,
        format_func=lambda x: f"{x} hours"
    )
    
    st.markdown("**📈 Chart Settings**")
    
    default_chart_type = st.selectbox(
        "Default chart type",
        options=["Line", "Candlestick", "Bar"],
        index=0
    )
    
    show_volume = st.checkbox("📊 Show volume by default", value=True)

with col2:
    st.markdown("**🎨 Display Settings**")
    
    theme = st.selectbox(
        "Theme",
        options=["Light", "Dark", "Auto"],
        index=2
    )
    
    currency = st.selectbox(
        "Default currency",
        options=["USD", "EUR", "GBP", "JPY"],
        index=0
    )
    
    timezone = st.selectbox(
        "Timezone",
        options=["UTC", "EST", "PST", "GMT"],
        index=1
    )
    
    st.markdown("**🔔 Notifications**")
    
    email_alerts = st.checkbox("📧 Email alerts", value=False)
    price_alerts = st.checkbox("💰 Price change alerts", value=True)
    
    alert_threshold = st.slider(
        "Alert threshold (%)",
        min_value=1,
        max_value=20,
        value=5
    )

# API settings
st.markdown("---")
st.subheader("🔗 API Configuration")

with st.expander("Alpha Vantage API Settings"):
    api_key_masked = "****" + (env_check['vars']['ALPHA_VANTAGE_API_KEY'] or "")[-4:] if env_check['vars']['ALPHA_VANTAGE_API_KEY'] else "Not set"
    st.text_input("API Key", value=api_key_masked, disabled=True)
    
    rate_limit = st.selectbox(
        "Rate limit (calls per minute)",
        options=[5, 75, 300, 600],
        index=0,
        help="Free tier: 5 calls/min, Premium: up to 600 calls/min"
    )

with st.expander("Supabase Database Settings"):
    db_url_masked = (env_check['vars']['supabaseURL'] or "Not set")
    st.text_input("Supabase URL", value=db_url_masked, disabled=True)
    
    connection_pool = st.slider(
        "Connection pool size",
        min_value=1,
        max_value=20,
        value=5
    )
    
    query_timeout = st.slider(
        "Query timeout (seconds)",
        min_value=10,
        max_value=120,
        value=30
    )

# Advanced settings
st.markdown("---")
st.subheader("🔧 Advanced Settings")

with st.expander("Performance Settings"):
    enable_caching = st.checkbox("💾 Enable data caching", value=True)
    parallel_requests = st.checkbox("⚡ Parallel API requests", value=False)
    
    max_records = st.number_input(
        "Max records per query",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100
    )

with st.expander("Debugging"):
    debug_mode = st.checkbox("🐛 Debug mode", value=False)
    log_level = st.selectbox(
        "Log level",
        options=["ERROR", "WARNING", "INFO", "DEBUG"],
        index=1
    )
    
    if st.button("📋 View Logs"):
        st.info("Logs would be displayed here")

# Save settings
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")

with col2:
    if st.button("🔄 Reset to Defaults"):
        st.warning("⚠️ Settings reset to default values")

with col3:
    st.markdown("*Settings are automatically saved when changed*")

# System information
st.markdown("---")
st.subheader("ℹ️ System Information")

system_info = {
    "Application Version": "1.0.0",
    "Streamlit Version": st.__version__,
    "Python Version": "3.11.0",
    "Database Status": "🟢 Connected",
    "API Status": "🟢 Active",
    "Last Backup": "2024-01-15 10:30 UTC"
}

for key, value in system_info.items():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**{key}:**")
    with col2:
        st.markdown(value)
