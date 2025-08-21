from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
from newspaper import Article
from readability import Document
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OpenAI_key"))
model="gpt-4o-mini"

def get_news_analysis(news_text):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": news_text}]
    )
    return response.choices[0].message.content

def scrape_with_readability(url):
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    doc = Document(resp.text)
    return doc.summary() 

def scrape_webpage(url):
    """Scrape full article text using newspaper3k"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"❌ Error scraping article: {e}")
        return None

def scrape_webpage_bs4(url):
    """Scrape content from a webpage"""
    MAX_CONTENT_LENGTH = 10000
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:MAX_CONTENT_LENGTH]  # Limit content length for API efficiency
    except Exception as e:
        return ("no news found")


def summarize_and_assess_industries(article_text):
    """
    Send news article content to OpenAI and get:
    - A concise summary
    - A list of positively and negatively impacted US industries
    """

    prompt = f"""
You are a market analyst AI for US businesses.

A user has provided a news article. Your task is to:
1. Summarize the article in 3–5 bullet points.
2. Identify **US industries** that could be impacted by this news.
3. Categorize them into:
   - **Positively impacted industries**
   - **Negatively impacted industries**

Format your answer as a JSON object with this structure:

{{
  "summary": ["point 1", "point 2", "..."],
  "positive_industries": ["Industry A", "Industry B"],
  "negative_industries": ["Industry X", "Industry Y"]
}}

News Article:
\"\"\"
{article_text}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        output_text = response.choices[0].message.content
        try:
            json_output = json.loads(output_text)
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON. Raw output:\n", output_text)
            return None
        return json_output

    except Exception as e:
        print(f"❌ Error analyzing article: {e}")
        return None


if __name__ == "__main__":
    news_link = "https://www.cnbctv18.com/technology/apple-expands-iphone-production-in-india-for-us-bound-new-models-ws-l-19655874.htm"
    text=scrape_with_readability(news_link)
    print(text)
    analysis=summarize_and_assess_industries(text)
    print(analysis)




