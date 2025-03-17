from web_search_agent import web_search_agent
from report_generator_agent import report_generator_agent
from langgraph.graph import StateGraph,MessagesState,END
from langchain_core.messages import HumanMessage,SystemMessage
import pprint

"""start making the router nodes to navigate between websearch and report generation """

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("web_search_agent",web_search_agent)
graph_builder.add_node("report_generator_agent",report_generator_agent)
graph_builder.add_edge("web_search_agent",END)
graph_builder.set_entry_point("web_search_agent")
graph = graph_builder.compile()

if __name__ == "__main__":
    response = graph.invoke({"messages": [HumanMessage(content="is dhoni the greatest captain?")]})
    pprint.pprint(response["messages"][-1].content)
    
"""make those 2 agents then create a main agent and then make them combined using command.
create a machine control that decides the transfer and then try it out for 
1. just websearch activity 
2. ask the question together.
3. add checkpointer and ask the question in couple of steps
"""