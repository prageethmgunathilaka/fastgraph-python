from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI(title="FastGraph API", description="A simple FastAPI application with LangGraph agent")

class AskRequest(BaseModel):
    text: str

@app.post("/ask")
async def ask(request: AskRequest):
    """Endpoint that accepts text and returns agent response."""
    # Run the LangGraph agent with the input text
    agent_response = run_agent(request.text)
    
    return {
        "received_text": request.text,
        "agent_response": agent_response
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to FastGraph API with LangGraph Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 