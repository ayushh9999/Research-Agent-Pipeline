"""Utility tools used by the agents in the ResearchMind pipeline.

This module defines small LangChain `@tool` wrappers for web search
and HTML scraping. Environment variables control external API keys:
- `TAVILY-API-KEY` for the Tavily search client.

The functions here are intentionally small and focused so they can be
invoked safely from agents.
"""

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

# Tavily client used to perform simple web searches. API key comes from
# the environment variable `TAVILY-API-KEY`.
tavily_client = TavilyClient(api_key=os.getenv("TAVILY-API-KEY"))

@tool
def web_search(query: str) -> str:
    """Perform a web search for recent and reliable information on a topic.
        Returns titles, URLs and snippets of the top search results.
    """
    results = tavily_client.search(query=query, max_results=5)
    
    out=[]
    
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n---\n".join(out)

#print(web_search.invoke("What is the latest research on multi-agent systems?"))

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading.
    """
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style', 'footer', 'nav']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
    
#print(scrape_url.invoke("https://github.com/kyegomez/awesome-multi-agent-papers"))