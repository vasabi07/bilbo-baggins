from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage


load_dotenv()
def web_search_agent(state: MessagesState):

    tavily_search = TavilySearchResults(max_results=3)
    llm = ChatOpenAI(model="gpt-4o")
    agent = create_react_agent(llm,tools=[tavily_search])
    response =agent.invoke({"messages":[HumanMessage(content=state["messages"][-1].content)]})
    return response
    
"""using tavily api as of now. must look for the best option.
consider giving prompt via state_modifier.

"""