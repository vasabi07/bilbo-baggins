from typing import TypedDict


class Message(TypedDict):
    type: str
    content: str
class MessagesState(TypedDict):
    messages: list[Message]
class RouterSchema(TypedDict):
    next_agent: str
