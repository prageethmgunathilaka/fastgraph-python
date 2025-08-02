from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FastGraph API", description="A simple FastAPI application")

class AskRequest(BaseModel):
    text: str

@app.post("/ask")
async def ask(request: AskRequest):
    """Endpoint that accepts text and returns hello world."""
    return {"message": "hello world", "received_text": request.text}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to FastGraph API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 