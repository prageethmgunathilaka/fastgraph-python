# FastGraph

A simple FastAPI application with LangGraph agent and LLM capabilities.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the environment template:
```bash
cp env_template.txt .env
```

2. Edit the `.env` file with your settings:
```env
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# LLM Configuration
DEFAULT_LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Important**: Replace `your-openai-api-key-here` with your actual OpenAI API key.

## Usage

Run the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - Welcome message
- `POST /ask` - Send text to LangGraph agent with LLM

## Access the API

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Example Request

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the capital of France?"}'
```

## Response Format

```json
{
  "received_text": "What is the capital of France?",
  "agent_response": "The capital of France is Paris..."
}
``` 