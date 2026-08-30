# langchain-demo

Personal learning/demo project for exploring LangChain and LangGraph basics.

## Setup

Requires Python >=3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file with the API keys used by the scripts:

```
GOOGLE_API_KEY=...
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

## Contents

- `src/langchain_demo/langchaininto.py` — basic LangChain/pydantic intro snippet.
- `src/langchain_demo/langraphbasic.py` — minimal LangGraph example: a `StateGraph` with a start node, a conditional-routing node, and two terminal branch nodes.
- `src/langchain_demo/langchainintro.ipynb` — notebook counterpart for interactive exploration.
- `src/langraphtools/chatbot_tools.py` — LangGraph tool-calling chatbot: a Groq LLM bound to Arxiv, Wikipedia, and Tavily search tools, with a `tools` node that loops back to the `llm` node so it can read tool results and produce a final answer.

## Running

```bash
uv run src/langchain_demo/langraphbasic.py
uv run src/langraphtools/chatbot_tools.py
```
