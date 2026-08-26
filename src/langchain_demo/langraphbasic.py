import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
import random
from typing import Literal

from langgraph.graph import StateGraph, START, END
from IPython.display import display, Image

load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

# StateSchema serves as as the input schema for all the nodes and edges in the graph
# It is used to store and pass the data between the nodes
class State(TypedDict):
    graph_info:str


def start_play(state: State):
    """Start the graph"""
    print("Start play node has been called!")
    return {"graph_info": state["graph_info"] + "Start play node has been executed!"}

def cricket(state: State):
    """cricket node has been called"""
    print("cricket node has been called!")
    return {"graph_info": state["graph_info"] + "cricket node has been executed!"}

def football(state: State):
    """football node has been called"""
    print("football node has been called!")
    return {"graph_info": state["graph_info"] + "football node has been executed!"}

# def end_game(state: State):
#     """end game node has been called"""
#     print("end game node has been called!")
#     return {"graph_info": state["graph_info"] + "end game node has been executed!"}


def random_play(state: State) -> Literal["cricket", "football"]:
    """random play node has been called"""
    print("random play node has been called!")
    if random.random() > 0.5:
        return "cricket"
    else:
        return "football"


# Build Graph
graph = StateGraph(State)

graph.add_node("start_play", start_play)
graph.add_node("cricket", cricket)
graph.add_node("football", football)

# Schedule the flow of graph
graph.add_edge(START, "start_play")
graph.add_conditional_edges("start_play", random_play)
graph.add_edge("cricket", END)
graph.add_edge("football", END)

# Compile the graph
graph_builder=graph.compile()

#view
# display(graph_builder.get_graph().draw_mermaid_png())

graph_builder.invoke({"graph_info":"My name is krish"})




