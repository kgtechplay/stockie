"""Stockie - Streamlit application entry point.

This homepage displays a banner and provides a search box that queries
the ``get_ticker_fuzzy`` function once the user enters at least three
characters. Results are shown in a dropdown and selecting one displays
the associated data.
"""

import os
import sys

import streamlit as st

# Allow importing from this directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.config import setup_page_config
from utils.auth import check_environment_variables


def main() -> None:
    """Render the Streamlit home page."""

    setup_page_config()

    # Ensure required environment variables exist
    env_check = check_environment_variables()
    if not env_check["all_set"]:
        st.error("⚠️ Environment Configuration Required")
        st.markdown(
            "Please configure the following environment variables in your `.env` file:"
        )
        for var, status in env_check["missing"].items():
            if not status:
                st.markdown(f"- `{var}`")
        st.stop()

    # Banner at the top
    banner_path = os.path.join("assets", "images", "stockie-banner.png")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)

    # Search input
    st.markdown("### Stock Analysis for a Company")
    query = st.text_input("Enter Company Name", key="search_box")

    results = []
    if len(query) >= 3:
        # Import here to avoid unnecessary Supabase calls before needed
        from get_ticker import get_ticker_fuzzy

        results = get_ticker_fuzzy(query)

    if len(query) > 0 and len(query) < 3:
        st.info("Enter at least 3 characters to search")

    if results:
        # Map display strings to result rows
        options = {
            f"{row[1]} - {row[3]} ({row[2]})": row for row in results
        }
        choice = st.selectbox(
            "Matching stocks", list(options.keys()), key=f"select_{query}"
        )
        if choice:
            selected = options[choice]
            st.write(
                {
                    "cik": selected[0],
                    "ticker": selected[1],
                    "exchange": selected[2],
                    "name": selected[3],
                }
            )
    elif len(query) >= 3:
        st.warning("No results found")


if __name__ == "__main__":
    main()
