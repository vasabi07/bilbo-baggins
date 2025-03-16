from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, END, START
from langchain_openai import ChatOpenAI
from web_search_agent import web_search_agent  # Import the web search agent
import pprint

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

class ReportSchema(TypedDict):
    question: str

class PlannerSchema(TypedDict):
    topics: List[str]

def question_node(state: MessagesState) -> ReportSchema:
    """Extract the question from user input."""
    question_text = state["messages"][-1].content  # Get the latest message
    print(f"Extracted Question: {question_text}")
    return {"question": question_text}

def research_node(state: ReportSchema) -> MessagesState:
    """Use the Web Search Agent to find relevant information about the question."""
    search_state = {"messages": [AIMessage(content=f"Search: {state['question']}")]}
    search_result = web_search_agent(search_state).invoke(search_state)
    
    # Store the search result in a message state
    return {"messages": [HumanMessage(content=search_result["messages"][-1].content)]}

def planner_node(state: MessagesState) -> PlannerSchema:
    """Plan research topics based on search results."""
    search_results = state["messages"][-1].content  # Get the web search results

    system_prompt = f"""
    Based on the following research results:
    {search_results}
    Identify and list the key topics that need further research.
    Output a structured list of research topics.
    """

    # Use LLM to generate research topics
    topics_response = llm.invoke([HumanMessage(content=system_prompt)])
    topics = [topic.strip() for topic in topics_response.content.split(",")]  # Ensure topics are a list of strings
    print(f"Generated Topics: {topics}")

    return {"topics": topics}

# ✅ Build the Graph (No Report Generation Yet)
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("question_node", question_node)
graph_builder.add_node("research_node", research_node)
graph_builder.add_node("planner_node", planner_node)

graph_builder.add_edge("question_node", "research_node")
graph_builder.add_edge("research_node", "planner_node")
graph_builder.add_edge("planner_node", END)
graph_builder.set_entry_point("question_node")

graph = graph_builder.compile()

if __name__ == "__main__":
    response = graph.invoke({"messages": [HumanMessage(content="Write a report on Dhoni the cricketer.")]})
    # pprint.pprint(response["messages"][-1].content)  