"""create an api endpoint for the main graph to contact FE"""
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from main import graph
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class Request_type(BaseModel):
    # threadId: str
    message: str


@app.post("/chat")
async def chat(request: Request_type):
    response =await graph.ainvoke({"messages": [HumanMessage(content=request.message)]})
    print(response["messages"][-1].content)
    reply = response["messages"][-1].content
    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)