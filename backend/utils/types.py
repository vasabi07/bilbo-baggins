from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class Message(TypedDict):
    role: str
    content: str
class MessagesState(TypedDict):
    messages: list[Message]
class RouterSchema(TypedDict):
    next_agent: str
