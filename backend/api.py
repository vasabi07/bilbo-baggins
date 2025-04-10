
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from utils.types import Message
from typing import TypedDict
from typing_extensions import NotRequired
import uuid 
from main import graph
from redis_store import conversation_store

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Request_type(TypedDict):
    threadId: NotRequired[str]
    message: str

def create_thread_id() -> str:
    return str(uuid.uuid4())

@app.post("/chat")
async def chat(request: Request_type):
    if request.get("threadId", "") == "":
        request["threadId"] = create_thread_id()
    # config = {"configurable": {"thread_id": request["threadId"]}}
    print(request["threadId"])
    previous_state = conversation_store.get_history(request["threadId"])
    previous_state["messages"].append(Message(role="user",content=request["message"]))
    print(f"input to the agent: {previous_state}")
    response =await graph.ainvoke(previous_state)
    conversation_store.save_history(request["threadId"], response)
    print(f"output from the agent: {response}")
    reply = response["messages"][-1]["content"]
    return {"threadId":request["threadId"],"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)