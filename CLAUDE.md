# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a personal learning/demo repo for LangChain and LangGraph basics. It is early-stage: scripts are exploratory, not a packaged application, and there is no test suite yet.

## Environment and commands

- Package/dependency management is via `uv` (see `uv.lock`, `pyproject.toml`). Python `>=3.12` (pinned to 3.12 in `.python-version`).
- Install/sync dependencies: `uv sync`
- Run a script: `uv run src/langchain_demo/langraphbasic.py` (or `langchaininto.py`)
- `requirements.txt` also exists and lists a subset of the same deps (langchain, langchain-community, langchain-core, langchain-openai, langchain-google-genai, langchain-groq, python-dotenv) — `pyproject.toml`/`uv.lock` is the source of truth; keep `requirements.txt` in sync if it's still needed.
- API keys (`GOOGLE_API_KEY`, `GROQ_API_KEY`, `TAVILY_API_KEY`) are stored in `.env` (gitignored) and loaded via `python-dotenv`. Never commit real key values.

## Code structure

- `src/langchain_demo/langchaininto.py` — basic LangChain/pydantic intro snippet.
- `src/langchain_demo/langraphbasic.py` — a minimal LangGraph example: builds a `StateGraph` with a shared `State` TypedDict, a start node, a conditional-routing node (`random_play`), and two terminal branch nodes (`cricket`, `football`), then compiles and invokes the graph. Useful as the reference pattern for any new LangGraph scripts in this repo (define `State`, define node functions that return partial state updates, wire nodes with `add_node`/`add_edge`/`add_conditional_edges`, `compile()`, `invoke()`).
- `src/langchain_demo/langchainintro.ipynb` — notebook counterpart for interactive exploration of the same concepts.
- `src/langchain_demo/__init__.py` — defines `main()`, the entry point referenced by the `langchain-demo` script in `pyproject.toml`.
- `src/langraphtools/chatbot_tools.py` — LangGraph tool-calling chatbot example: binds a Groq LLM (`llm_with_tools`) to Arxiv, Wikipedia, and Tavily search tools via `bind_tools`, then wires a `StateGraph` with an `llm` node and a `ToolNode("tools")`. `tools_condition` routes conditionally from `llm` to either `tools` or `END`; the `tools` edge loops back to `llm` (not `END`) so the model can read tool output and produce a final natural-language answer. The `State` TypedDict's key must exactly match what nodes read/write and what `graph.invoke(...)` passes (`messages`) — a mismatched key name causes a `KeyError` inside the node since LangGraph won't populate an undeclared state key.
