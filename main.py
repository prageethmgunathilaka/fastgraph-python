from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union, Any
from agents import run_agent, run_workflow_agent, run_orchestrate_agent, run_auto_orchestrate_agent
from config import Config

app = FastAPI(title="FastGraph API", description="A simple FastAPI application with LangGraph agent")

class AskRequest(BaseModel):
    text: str

class WorkflowAskRequest(BaseModel):
    commands: List[str]

class OrchestrateRequest(BaseModel):
    tasks: List[List[Union[str, List[Any]]]]

class AutoOrchestrateRequest(BaseModel):
    command: str

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
    """Endpoint that accepts a list of commands and returns workflow agent responses with summary."""
    # Run the workflow agent with the list of commands
    workflow_responses, finalized_result = run_workflow_agent(request.commands)
    
    return {
        "received_commands": request.commands,
        "workflow_responses": workflow_responses,
        "finalizedResult": finalized_result
    }

@app.post("/orchestrate")
async def orchestrate(request: OrchestrateRequest):
    """Endpoint that accepts hierarchical tasks and returns orchestrated responses."""
    # Run the orchestrate agent with the hierarchical tasks
    orchestrate_responses, finalized_result = run_orchestrate_agent(request.tasks)
    
    return {
        "received_tasks": request.tasks,
        "orchestrate_responses": orchestrate_responses,
        "finalizedResult": finalized_result
    }

@app.post("/autoOrchestrate")
async def auto_orchestrate(request: AutoOrchestrateRequest):
    """Endpoint that automatically determines roles and creates agent swarms for a command."""
    # Run the auto orchestrate agent with the command
    auto_orchestrate_response, finalized_result = run_auto_orchestrate_agent(request.command)
    
    return {
        "received_command": request.command,
        "auto_orchestrate_response": auto_orchestrate_response,
        "finalizedResult": finalized_result
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to FastGraph API with LangGraph Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 