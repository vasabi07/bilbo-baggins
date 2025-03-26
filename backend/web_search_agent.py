from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from utils.llm import llm
from utils.types import Message, MessagesState
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import json

load_dotenv()

tavily_search = TavilySearchResults(max_results=3)

class AgentState(TypedDict):
    messages: List[Message]
    tool_results: str

def web_search_agent(state: AgentState):

    def decide_action(state: AgentState) -> Dict[str, str]:
        query = state["messages"][-1]["content"]
        
        system_prompt = f"""
        Given the query: "{query}", decide whether to:
        - Use a tool (if external information is needed)
        - Respond directly (if LLM already knows the answer)
        
        Reply with either:
        - "USE_TOOL"
        - "RESPOND_DIRECTLY"
        """

        decision = llm(system_prompt).content.strip().upper()
        result = {"next_step": "use_tool" if decision == "USE_TOOL" else "respond_directly"}
        return result 

    def execute_tool(state: AgentState) -> AgentState:
        query = state["messages"][-1]["content"]
        tool_output = tavily_search.invoke(query)  

        return {
            "messages": state["messages"],
            "tool_results": json.dumps(tool_output, indent=2),
        }

    def generate_response(state: AgentState) -> MessagesState:
        query = state["messages"][-1]["content"]
        
        tool_context = f"\n\nHere are the search results:\n{state['tool_results']}" if state.get("tool_results") else ""
        
        system_prompt = f"""
        You are a helpful assistant. Answer the following query:

        {query}

        {tool_context}

        Provide a well-structured and concise response.
        """

        response_text = llm(system_prompt).content  
        return {"messages": state["messages"] + [Message(type="AI", content=response_text)]}

    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("decide_action", decide_action)
    graph_builder.add_node("use_tool", execute_tool)
    graph_builder.add_node("respond_directly", generate_response)

    graph_builder.add_conditional_edges(
        "decide_action",
        lambda state: state["next_step"], 
        {
            "use_tool": "use_tool",
            "respond_directly": "respond_directly",
        }
    )

    graph_builder.add_edge("use_tool", "respond_directly") 
    graph_builder.add_edge("respond_directly", END)  

    graph_builder.set_entry_point("decide_action")
    web_search_graph = graph_builder.compile()
    response = web_search_graph.invoke({"messages": [Message(type="human", content=state["messages"][-1]["content"])]})
    return response


# if __name__ == "__main__":
#     user_query = "When is CSK vs RCB 2025?"
#     print(response["messages"][-1]["content"])  
