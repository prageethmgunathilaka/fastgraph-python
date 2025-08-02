from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agent import run_agent
from workflow_agent import run_workflow_agent
from config import Config

app = FastAPI(title="FastGraph API", description="A simple FastAPI application with LangGraph agent")

class AskRequest(BaseModel):
    text: str

class WorkflowAskRequest(BaseModel):
    commands: List[str]

@app.post("/ask")
async def ask(request: AskRequest):
    """Endpoint that accepts text and returns agent response."""
    # Run the LangGraph agent with the input text
    agent_response = run_agent(request.text)
    
    return {
        "received_text": request.text,
        "agent_response": agent_response
    }

@app.post("/workflowask")
async def workflow_ask(request: WorkflowAskRequest):
    """Endpoint that accepts a list of commands and returns workflow agent responses."""
    # Run the workflow agent with the list of commands
    workflow_responses = run_workflow_agent(request.commands)
    
    return {
        "received_commands": request.commands,
        "workflow_responses": workflow_responses
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to FastGraph API with LangGraph Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 