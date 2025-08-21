import streamlit as st
import sys
import os
import json
from openAI_news import scrape_webpage, summarize_and_assess_industries
from utils.config import setup_page_config
from utils.auth import check_environment_variables

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure page
setup_page_config()

# Check environment variables
env_check = check_environment_variables()
if not env_check['all_set']:
    st.error("⚠️ Environment variables not configured. Please check your .env file.")
    st.stop()

def main():
    st.title("📰 News Analyzer")
    st.markdown("---")
    
    st.markdown("### 🔍 Analyze News Content")
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'scraped_text' not in st.session_state:
        st.session_state.scraped_text = None
    
    # News input
    news_url = st.text_input(
        "Enter news content link to analyze:",
        placeholder="Paste news link that we want to analyze...",
        key="news_input"
    )
    
    # Analysis button
    if st.button("🚀 Analyze News", type="primary", disabled=not news_url.strip()):
        if news_url.strip():
            with st.spinner("🔍 Scraping webpage..."):
                # Scrape the webpage
                scraped_text = scrape_webpage(news_url)
                st.session_state.scraped_text = scraped_text
                
                if scraped_text == "no news found":
                    st.error("❌ Could not scrape content from the provided URL. Please check the link and try again.")
                else:
                    st.success("✅ Webpage scraped successfully!")
                    
                    with st.spinner("🤖 Analyzing content with AI..."):
                        # Analyze the scraped text
                        analysis_results = summarize_and_assess_industries(scraped_text)
                        st.session_state.analysis_results = analysis_results
                        
                        if analysis_results:
                            st.success("✅ Analysis completed!")
                        else:
                            st.error("❌ Analysis failed. Please try again.")
        else:
            st.warning("Please enter a URL to analyze.")
    
    # Display results
    if st.session_state.analysis_results:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Summary section
        if 'summary' in results:
            st.markdown("#### 📝 Summary")
            for i, point in enumerate(results['summary'], 1):
                st.markdown(f"• {point}")
        
        # Positive industries
        if 'positive_industries' in results and results['positive_industries']:
            st.markdown("#### 🟢 Positively Impacted Industries")
            for industry in results['positive_industries']:
                st.markdown(f"✅ {industry}")
        
        # Negative industries
        if 'negative_industries' in results and results['negative_industries']:
            st.markdown("#### 🔴 Negatively Impacted Industries")
            for industry in results['negative_industries']:
                st.markdown(f"❌ {industry}")
        
        # Raw JSON view (expandable)
        with st.expander("🔍 View Raw Analysis Data"):
            st.json(results)
    
    # Display scraped text (expandable)
    if st.session_state.scraped_text and st.session_state.scraped_text != "no news found":
        with st.expander("📄 View Scraped Content"):
            st.text(st.session_state.scraped_text[:1000] + "..." if len(st.session_state.scraped_text) > 1000 else st.session_state.scraped_text)

if __name__ == "__main__":
    main()
