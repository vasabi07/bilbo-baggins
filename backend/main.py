from web_search_agent import web_search_agent
from report_generator_agent import report_generator_agent
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from typing import Literal
from utils.llm import llm
from dotenv import load_dotenv
from utils.types import Message, MessagesState, RouterSchema
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

def classifier(state: MessagesState) -> RouterSchema:
    question = state["messages"][-1]["content"]
    system_prompt = f"""
    You are a professional classifier. You should read the question: "{question}" and classify it to whether it needs to go into "web search", 
    "report generation" or "neither".
    Report-generator examples:
    "Whenever you are asked to do a research or write a report or deep research, you should strictly mark it as a report-generator even if it requires 
    to do a web search before writing the report because the report generator can do websearch as well.
    1. Do a detailed research on the recently released MacBook M4.
    2. Write a report on the recent fire in LA."
    3. Who is the current Indian captain in cricket and write a report on him.
    4. I want to learn deeply about AI.
    Web-search examples:
    "All recent activities that need to be searched online to make sure the answer is correct need to be marked as websearch."
    1. What is the weather today?
    2. What is the score for the IND vs PAK game?
    3. What movies are running near my location?

    Please reply with "report generation" or "web search" or "neither".
    Do not explain the reasoning behind them. I strictly want only one of these three to be the response.
    """
    response = llm([Message(role="system", content=system_prompt)])
    content = response.content.lower()

    if "report generation" in content:
        next_agent = "report_generator_agent"
    elif "web search" in content:
        next_agent = "web_search_agent"
    else:
        next_agent = "neither"
    
    return {"next_agent": next_agent}

def simple_node(state: MessagesState) -> MessagesState:
    
    last_message = state["messages"][-1]["content"]
    response = llm(state["messages"])
    state["messages"].append(Message(role="AI", content=response.content))
    print(state)
    return {"messages": [Message(role="AI", content=response.content)]}
    
def router(state: RouterSchema) -> Command[Literal["web_search_agent", "report_generator_agent", "__end__"]]:
    goto = state["next_agent"]
    if goto == "neither":
        goto = "simple_node"
    return Command(goto=goto)

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("web_search_agent", web_search_agent)
graph_builder.add_node("report_generator_agent", report_generator_agent)
graph_builder.add_node("simple_node", simple_node)
graph_builder.add_node("classifier", classifier)
graph_builder.add_node("router", router)
graph_builder.add_edge("classifier", "router")
graph_builder.add_edge("web_search_agent", END)
graph_builder.add_edge("report_generator_agent", END)
graph_builder.add_edge("simple_node", END)
graph_builder.set_entry_point("classifier")
graph = graph_builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    response = graph.invoke(
        {"messages": [Message(type="HUMAN", content="hi, I am vasanth")]},
        config={"configurable": {"thread_id": 1}}
    )
    print(response)
    response2 = graph.invoke(
        {"messages": [Message(type="HUMAN", content="what is my name")]},
        config={"configurable": {"thread_id": 1}}
    )
    print(response2)
