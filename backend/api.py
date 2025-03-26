"""create an api endpoint for the main graph to contact FE,
use checkpointer and connect to a DB may be something like redis for faster retrieval

"""
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
    if request.threadId == "":
        request.threadId = create_thread_id()
    #must add threadId logic with checkpointer from langgraph 
    response =await graph.ainvoke({"messages": [Message(type="Human",content=request.message)]})
    print(response["messages"][-1].content)
    reply = response["messages"][-1].content
    return {"threadId":request.threadId,"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)