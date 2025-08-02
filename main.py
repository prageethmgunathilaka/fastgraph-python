from fastapi import FastAPI

app = FastAPI(title="FastGraph API", description="A simple FastAPI application")

@app.get("/ask")
async def ask():
    """Endpoint that always returns hello world."""
    return {"message": "hello world"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to FastGraph API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 