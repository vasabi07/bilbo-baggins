from dotenv import load_dotenv
from typing import TypedDict, List
from typing_extensions import NotRequired
from utils.types import Message,MessagesState
from utils.llm import llm
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from web_search_agent import web_search_agent
import pprint

load_dotenv()

"""improvements required:
                1. human in the loop to verify after planning stage and make changes
                2. some kind of re-write loop, that checks if everything is written as per the plan.
                3. make the research part parallel
                4.add a seperate python_repl tool, so that it can create charts and graphs if it is necessary for the report.

"""



class ReportSchema(TypedDict):
    question: str
    report: NotRequired[str]
    gathered_info: NotRequired[str]

class PlannerSchema(TypedDict):
    topics: List[str]

def report_generator_agent(state: MessagesState):

    def question_node(state: MessagesState) -> ReportSchema:
        print(state)
        question_text = state["messages"][-1]["content"]
        print(f"Extracted Question: {question_text}")
        return {"question": question_text}

    def research_node(state: ReportSchema) -> MessagesState:
        search_state = {"messages": [Message(type="AI",content=f"Search: {state['question']}")]}
        search_result = web_search_agent(search_state)
        return {"messages": [Message(type="Human",content=search_result["messages"][-1]["content"])]}

    def planner_node(state: MessagesState) -> PlannerSchema:
        search_results = state["messages"][-1]["content"]
        system_prompt = f"""
        Based on the following research results:
        {search_results}
        Identify and list the key topics that need further research.
        Output a structured list of research topics.
        """
        topics_response = llm(system_prompt)
        topics = [topic.strip() for topic in topics_response.content.split(",")]
        return {"topics": topics}

    def gathering_info(state: PlannerSchema) -> ReportSchema:
        topics = state["topics"]
        gathered_info = []
        for topic in topics:
            system_prompt = f"""
            For the topic: {topic}, gather information on it. This is part of a big report. Your job is to work only on this topic.
            """
            search_result = web_search_agent({"messages": [Message(type="Human",content=system_prompt)]})
            gathered_info.append(search_result["messages"][-1]["content"])
        return {"gathered_info": gathered_info}

    def report_generation(state: ReportSchema) -> MessagesState:
        system_prompt = f"""
        Generate an extensive report with the given info on the question {state['question']},
        make sure to include introduction, conclusion, and topics in between.
        Provide the links if available at the end as references.
        """
        gathered_info_str = "\n".join(state["gathered_info"])
        full_prompt = system_prompt + "\n\n" + gathered_info_str
        report_response = llm(full_prompt)
        report_content = report_response.content
        return {"messages": [Message(type="AI",content=report_content)]}

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("question_node", question_node)
    graph_builder.add_node("research_node", research_node)
    graph_builder.add_node("planner_node", planner_node)
    graph_builder.add_node("gathering_info",gathering_info)
    graph_builder.add_node("report_generation",report_generation)

    graph_builder.add_edge("question_node", "research_node")
    graph_builder.add_edge("research_node", "planner_node")
    graph_builder.add_edge("planner_node","gathering_info")
    graph_builder.add_edge("gathering_info","report_generation")
    graph_builder.add_edge("report_generation", END)
    graph_builder.set_entry_point("question_node")

    graph = graph_builder.compile()
    response = graph.invoke({"messages":[Message(type="Human",content=state["messages"][-1]["content"])]})
    return response

# if __name__ == "__main__":
#     response = report_generator_agent({"messages": [Message(type="Human",content="what is AI engineering?")]})
#     pprint.pprint(response)
