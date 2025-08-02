# FastGraph

A simple FastAPI application with LangGraph agent and LLM capabilities.

## Project Structure

```
fastgraph/
├── agents/                 # Agent implementations
│   ├── __init__.py        # Package exports
│   ├── regular_agent.py   # Single command agent
│   └── workflow_agent.py  # Multi-command workflow agent
├── config.py              # Configuration management
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies
├── test/                  # Test suite
│   ├── test_ask_endpoint.py
│   ├── test_workflow_endpoint.py
│   └── test_workflow_integration.py
└── README.md
```

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

### `/ask` - Single Command Agent
- **Method**: POST
- **Request**: `{"text": "your command"}`
- **Response**: `{"received_text": "...", "agent_response": "..."}`

### `/workflowask` - Workflow Agent
- **Method**: POST
- **Request**: `{"commands": ["cmd1", "cmd2", "cmd3"]}`
- **Response**: `{"received_commands": [...], "workflow_responses": [...], "finalizedResult": "summary"}`

## Access the API

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Example Requests

### Single Command
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the capital of France?"}'
```

### Workflow Commands
```bash
curl -X POST "http://localhost:8000/workflowask" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [
      "What is the capital of France?",
      "Calculate 2 + 2",
      "Translate hello to Spanish"
    ]
  }'
```

## Testing

Run the integration tests:

```bash
# Run all tests
pytest test/ -v

# Run specific test
python test/test_workflow_integration.py

# Run with verbose output
pytest test/ -v
```

## Library Structure

The agents are organized as a reusable library:

```python
from agents import run_agent, run_workflow_agent

# Single command processing
response = run_agent("What is 2 + 2?")

# Multiple command processing
responses, summary = run_workflow_agent([
    "What is the capital of France?",
    "Calculate 15 + 27",
    "Translate hello to Spanish"
])
```

## Architecture

- **Regular Agent**: Processes single commands through LLM
- **Workflow Agent**: Orchestrates multiple regular agents and creates summaries
- **Configuration**: Centralized environment-based configuration
- **Testing**: Comprehensive integration test suite 