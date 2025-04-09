
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from utils.types import Message
from typing import TypedDict
from typing_extensions import NotRequired
import uuid 
from main import graph


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
    config = {"configurable": {"thread_id": request["threadId"]}}
    response =await graph.ainvoke({"messages": [Message(role="user",content=request["message"])]},config=config)
    print(response["messages"])
    reply = response["messages"][-1]["content"]
    return {"threadId":request["threadId"],"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)