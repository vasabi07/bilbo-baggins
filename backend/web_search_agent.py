from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from utils.llm import llm
from utils.types import Message, MessagesState
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import json
from typing_extensions import NotRequired

load_dotenv()

tavily_search = TavilySearchResults(max_results=3)

class AgentState(TypedDict):
    messages: List[Message]
    tool_results: NotRequired[str]
    query: NotRequired[str]
    next_step: NotRequired[str]

def web_search_agent(state: AgentState):
    def decide_action(state: AgentState) -> Dict[str, str]:
        query = state["messages"][-1]["content"]
        state["query"] = query
        system_prompt = f"""
        Given the query: "{query}", decide whether to:
        - Use a tool (if external information is needed)
        - Respond directly (if LLM already knows the answer)
        
        Reply with either:
        - "USE_TOOL"
        - "RESPOND_DIRECTLY"
        """
        # Append the system prompt as a new message
        state["messages"].append(Message(role="system", content=system_prompt))
        decision = llm(state["messages"]).content.strip().upper()
        # result = {"next_step": "use_tool" if decision == "USE_TOOL" else "respond_directly"}
        state["next_step"] = "use_tool" if decision == "USE_TOOL" else "respond_directly"

        return state 

    def execute_tool(state: AgentState) -> AgentState:
        query = state["query"]
        tool_output = tavily_search.invoke(query)  
        return {
            "messages": state["messages"],
            "tool_results": json.dumps(tool_output, indent=2),
            "query": state["query"],
            "next_step": state["next_step"]
        }

    def generate_response(state: AgentState):
        query = state["query"]
        tool_context = f"\n\nHere are the search results:\n{state['tool_results']}" if state.get("tool_results") else ""
        system_prompt = f"""
        You are a helpful assistant. Answer the following query:

        {query}

        {tool_context}

        Provide a well-structured and concise response.
        """
        response_text = llm([{"role": "system", "content": system_prompt}]).content

        # Return a new state with the agent's final message appended
        # state["messages"].append(Message(role="AI", content=response_text))
        new_state = {
        "messages": state["messages"] + [Message(role="AI", content=response_text)],
        "tool_results": state.get("tool_results", ""),
        "query": state["query"],
        "next_step": state["next_step"]
    }
        return new_state

    # Build the agent's internal graph
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
    
    # Invoke the agent using only the latest human message
    agent_state = web_search_graph.invoke({
        "messages": [Message(role="user", content=state["messages"][-1]["content"])]
    })
    # Extract the final output from the agent
    final_agent_message = agent_state["messages"][-1]
    # Append the final message into the main state
    state["messages"].append(final_agent_message)
    return state

