# ResearchMind — Multi-Agent Research Pipeline

ResearchMind is a lightweight multi-agent research assistant built with LangChain and Google Gemini (via langchain-google-genai). It coordinates specialized agents to search the web, scrape and extract content, draft a structured research report, and critique the draft — all exposed via a Streamlit UI and a CLI runner.

Key goals:
- Rapidly synthesize reliable, sourced research reports.
- Provide reproducible, modular pipeline stages for experimentation.
- Easy local setup and deployment using Streamlit.

---

## Features

- Multi-agent pipeline: Search → Reader (scrape) → Writer → Critic
- Streamlit UI for interactive runs and a CLI entrypoint for automation
- Small, focused tool wrappers for search and scraping
- Environment-configurable model and API keys

---

## Quick Start (local development)

Prerequisites:
- Python 3.10+ recommended
- A virtual environment (recommended)
- API keys for the LLM (`GEMINI_API_KEY`) and the Tavily search client (`TAVILY-API-KEY`) if you want web search

1) Create and activate a virtual environment

```bash
python -m venv .venv
# PowerShell (Windows)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Create a `.env` file in the project root with required environment variables

```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
TAVILY-API-KEY=your_tavily_api_key_here
```

4) Run the Streamlit UI

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

5) Or run the CLI pipeline directly

```bash
python pipeline.py
# then enter a topic when prompted
```

---

## Configuration / Environment Variables

- `GEMINI_API_KEY` (required to use the Gemini models via the langchain integration)
- `GEMINI-API-KEY` (alternate name used by the code)
- `GEMINI_MODEL` (optional, defaults to `gemini-2.5-flash`)
- `TAVILY-API-KEY` (optional; required if using `web_search` tool)

Keep secrets in a `.env` file and ensure `.gitignore` contains `.env` (this repo includes a sensible `.gitignore`).

---

## File Overview

- `app.py` — Streamlit frontend and pipeline orchestration for UI users.
- `pipeline.py` — CLI runner that executes the pipeline and prints outputs.
- `agents.py` — Agent and chain construction (LLM, writer chain, critic chain).
- `tools.py` — Small `@tool` wrappers: `web_search` and `scrape_url`.
- `requirements.txt` — Python package dependencies.
- `.gitignore` — Project ignore rules.

---

## How it works (high-level)

1. The Search agent queries the web (via `web_search`) and returns relevant titles/URLs/snippets.
2. The Reader agent chooses a URL and scrapes its content (via `scrape_url`).
3. The Writer chain receives combined research text and drafts a structured report.
4. The Critic chain reviews the drafted report and produces scored feedback.

Agents communicate via LangChain's agent API and use the shared `llm` instance from `agents.py`.

---

## Tips & Best Practices

- Run in a dedicated virtualenv to avoid dependency conflicts.
- Start with `GEMINI_MODEL=gemini-2.5-flash` and `temperature=0` in `agents.py` for stable outputs.
- If you plan to publish the code, remove or rotate any real API keys from your environment and never commit them.
- For heavy scraping or production workloads, consider rate limits and respectful crawling (robots.txt) and caching results.

---

## Contributing

Contributions are welcome. A suggested workflow:

1. Fork the repo and create a feature branch.
2. Add tests or manual verification steps for behaviour you change.
3. Open a pull request with a clear description of the change.

---
