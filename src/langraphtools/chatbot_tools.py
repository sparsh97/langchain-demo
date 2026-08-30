import os
import wikipedia
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

wikipedia.set_user_agent("langchain-demo/0.1 (sparshv1989@gmail.com)")

#tools

api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Query arxiv papers based on keyword")

api_wrapper_wikipedia = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
# shadows the imported `wikipedia` module on purpose; module isn't used again after this point
wikipedia=WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia, description="Query wikipedia based on keyword")

tavily_search = TavilySearchResults()

tools = [arxiv,wikipedia,tavily_search]

#intialize llm model
llm = ChatGroq(model_name="qwen/qwen3.6-27b", temperature=0)
llm_with_tools = llm.bind_tools(tools=tools)


#workflow

class State(TypedDict):
    messages: list[Annotated[AnyMessage, add_messages]]


# node definition
def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# building graph
builder = StateGraph(State)
builder.add_node("llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

# edge definition

builder.add_edge(START, "llm")
# tools_condition routes to "tools" if the last message has tool calls, else to END
builder.add_conditional_edges(
    "llm",
    tools_condition
)
# loop back to "llm" so it can read tool results and produce a final answer
builder.add_edge("tools","llm")

graph = builder.compile()


# messages = graph.invoke({"messages":[HumanMessage(content="1706.03762")]})
messages = graph.invoke({"messages":[HumanMessage(content="my name is Sparsh")]})

for m in messages['messages']:
    m.pretty_print()

