"""agents.py

Constructs and exposes the LangChain agents and chains used by
the ResearchMind pipeline.

Exports:
- `build_search_agent()`  : Agent configured to perform web searches.
- `build_reader_agent()`  : Agent configured to scrape and extract page content.
- `writer_chain`         : Prompt+LLM chain that drafts a research report.
- `critic_chain`         : Prompt+LLM chain that reviews and scores a report.

This module reads API keys from the environment (see .env) and
initializes a Google Gemini LLM wrapper for use across chains.
"""

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

def _get_setting(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value

    try:
        import streamlit as st

        for name in names:
            value = st.secrets.get(name)
            if value:
                return value
    except Exception:
        pass

    return None


model_name = _get_setting("GEMINI_MODEL") or "gemini-2.5-flash"
gemini_api_key = _get_setting("GEMINI_API_KEY", "GEMINI-API-KEY")

llm = None
if gemini_api_key:
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        api_key=gemini_api_key,
        temperature=0
    )

# 1st agent (tavily search)
def build_search_agent():
    """Return an agent configured to perform web searches.

    The returned agent is wired to the `web_search` tool defined in
    `tools.py` and uses the shared `llm` instance. It accepts the
    standard LangChain agent invocation input (messages dict).
    """
    if llm is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to Streamlit secrets or your .env file."
        )

    return create_agent(model=llm, tools=[web_search])

# 2nd agent (scrape url)
def build_reader_agent():
    """Return an agent configured to scrape and extract content from a URL.

    The reader agent is intended to receive a URL or short instruction and
    use the `scrape_url` tool to fetch and return cleaned page text.
    """
    if llm is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to Streamlit secrets or your .env file."
        )

    return create_agent(model=llm, tools=[scrape_url])

#Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = (writer_prompt | llm | StrOutputParser()) if llm is not None else None

#Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = (critic_prompt | llm | StrOutputParser()) if llm is not None else None