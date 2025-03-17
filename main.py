from web_search_agent import web_search_agent
from report_generator_agent import report_generator_agent
from langgraph.graph import StateGraph, MessagesState, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict
import pprint


class RouterSchema(TypedDict):
    next_agent: str

def classifier(state: MessagesState) -> RouterSchema:
    question = state["messages"][-1].content
    system_prompt = f"""
    You are a professional classifier. You should read the question: "{question}" and classify it to whether it needs to go into "web search", 
    "report generation" or "neither".
    Report-generator examples:
    "Whenever you are asked to do a research or write a report or deep research, you should strictly mark it as a report-generator even if it requires 
    to do a web search before writing the report because the report generator can do websearch as well.
    1. Do a detailed research on the recently released MacBook M4.
    2. Write a report on the recent fire in LA."
    3.who is the current indian captian in cricket and write a report on him.
    4. I want to learn deeply about AI
    Web-search examples:
    "All recent activities that need to be searched online to make sure the answer is correct need to be marked as websearch."
    1. What is the weather today?
    2. What is the score for the IND vs PAK game?
    3. What movies are running near my location?

    please reply with "report generation" or "web search" or "neither"
    do not explain the resoning behind them. I strictly want only one of these three to be the response
    """
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke(system_prompt)
    content = response.content.lower()
    
    if "report generation" in content:
        next_agent = "report_generation"
    elif "web search" in content:
        next_agent = "web_search"
    else:
        next_agent = "neither"
    
    
    return {"next_agent": next_agent}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("web_search_agent", web_search_agent)
graph_builder.add_node("report_generator_agent", report_generator_agent)
graph_builder.add_edge("web_search_agent", END)
graph_builder.set_entry_point("web_search_agent")
graph = graph_builder.compile()

if __name__ == "__main__":
    response = classifier({"messages": [HumanMessage(content="what is the best theatre in chennai?")]})
    pprint.pprint(response)

"""make those 2 agents then create a main agent and then make them combined using command.
create a machine control that decides the transfer and then try it out for 
1. just websearch activity 
2. ask the question together.
3. add checkpointer and ask the question in couple of steps
"""