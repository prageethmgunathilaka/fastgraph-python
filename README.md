# FastGraph

A simple FastAPI application with LangGraph agent and LLM capabilities.

## Project Structure

```
fastgraph/
├── agents/                 # Agent implementations
│   ├── __init__.py        # Package exports
│   ├── regular_agent.py   # Single command agent
│   ├── workflow_agent.py  # Multi-command workflow agent
│   ├── orchestrate_agent.py # Hierarchical orchestration agent
│   └── auto_orchestrate_agent.py # Auto role detection and swarm creation
├── config.py              # Configuration management
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies
├── test/                  # Test suite
│   ├── test_ask_endpoint.py
│   ├── test_workflow_endpoint.py
│   ├── test_workflow_integration.py
│   ├── test_orchestrate_endpoint.py
│   └── test_auto_orchestrate_endpoint.py
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

### `/orchestrate` - Hierarchical Orchestration Agent
- **Method**: POST
- **Request**: `{"tasks": [["task1", "task2"], ["nested_task", ["subtask1", "subtask2"]], ["final_task"]]}`
- **Response**: `{"received_tasks": [...], "orchestrate_responses": [...], "finalizedResult": "summary"}`

### `/autoOrchestrate` - Auto Role Detection and Swarm Creation
- **Method**: POST
- **Request**: `{"command": "your command"}`
- **Response**: `{"received_command": "...", "auto_orchestrate_response": {...}, "finalizedResult": "..."}`

**Auto Orchestrate Features**:
- Automatically identifies the appropriate professional role for the command
- Generates M Language specifications for agent swarms
- Executes the swarm using the MParser runtime
- Returns processed results with role context

**Orchestrate Structure**:
- Each string in the tasks array goes to a regular agent
- Each array of strings becomes a workflow
- Workflows can spawn other workflows (nested structure)
- Results cascade up to create final summaries

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

### Orchestrate Tasks
```bash
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      ["Hello, how are you?", "What is the weather like?"],
      ["Explain quantum computing"],
      ["Write a poem", "Translate it to Spanish"]
    ]
  }'
```

### Auto Orchestrate Command
```bash
curl -X POST "http://localhost:8000/autoOrchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Analyze the current market trends for renewable energy"
  }'
```

### Complex Nested Orchestration
```bash
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      ["Research AI", ["Find AI papers", "Summarize findings"]],
      ["Write code", "Test code", ["Unit tests", "Integration tests"]],
      ["Deploy", ["Build", "Deploy to staging", "Deploy to production"]]
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
python test/test_orchestrate_endpoint.py
python test/test_auto_orchestrate_endpoint.py

# Run with verbose output
pytest test/ -v
```

## Library Structure

The agents are organized as a reusable library:

```python
from agents import run_agent, run_workflow_agent, run_orchestrate_agent, run_auto_orchestrate_agent

# Single command processing
response = run_agent("What is 2 + 2?")

# Multiple command processing
responses, summary = run_workflow_agent([
    "What is the capital of France?",
    "Calculate 15 + 27",
    "Translate hello to Spanish"
])

# Hierarchical orchestration
orchestrate_responses, summary = run_orchestrate_agent([
    ["Task 1", "Task 2"],  # Workflow
    ["Nested task", ["Subtask 1", "Subtask 2"]],  # Nested workflow
    ["Final task"]  # Single agent
])

# Auto orchestrate with role detection
auto_response, summary = run_auto_orchestrate_agent(
    "Create a Python script to scrape data from a website"
)
```

## Architecture

- **Regular Agent**: Processes single commands through LLM
- **Workflow Agent**: Orchestrates multiple regular agents and creates summaries
- **Orchestrate Agent**: Handles hierarchical workflows with nested structures
- **Auto Orchestrate Agent**: Automatically detects roles and creates agent swarms using M Language
- **Configuration**: Centralized environment-based configuration
- **Testing**: Comprehensive integration test suite 