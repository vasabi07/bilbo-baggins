"""create an api endpoint for the main graph to contact FE"""
from fastapi import Fastapi  
from fastapi.middleware.cors import CORSMiddleware

app = Fastapi()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


# @app.post("/chat")
# async def chat(request: )