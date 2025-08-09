# FastGraph API Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. `/ask` - Single Command Agent
**Method**: `POST`  
**Purpose**: Process a single command with a regular agent

**Request**:
```json
{
  "text": "your command here"
}
```

**Response**:
```json
{
  "received_text": "your command here",
  "agent_response": "AI response to your command"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the capital of France?"}'
```

---

### 2. `/workflowask` - Workflow Agent
**Method**: `POST`  
**Purpose**: Process multiple commands in sequence with workflow orchestration

**Request**:
```json
{
  "commands": ["command1", "command2", "command3"]
}
```

**Response**:
```json
{
  "received_commands": ["command1", "command2", "command3"],
  "workflow_responses": ["response1", "response2", "response3"],
  "finalizedResult": "Summary of all responses"
}
```

**Example**:
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

---

### 3. `/orchestrate` - Hierarchical Orchestration Agent
**Method**: `POST`  
**Purpose**: Process complex hierarchical workflows with nested agents and workflows

**Request Structure**:
```json
{
  "tasks": [
    ["task1", "task2"],                    // Simple workflow
    ["nested_task", ["subtask1", "subtask2"]],  // Nested workflow
    ["single_task"],                       // Single agent
    [["deep_nested", ["very_deep"]]]      // Deep nesting
  ]
}
```

**Response**:
```json
{
  "received_tasks": [...],
  "orchestrate_responses": [
    {
      "type": "workflow",
      "responses": ["response1", "response2"],
      "finalized_result": "workflow summary"
    },
    {
      "type": "nested_workflow", 
      "responses": [...],
      "finalized_result": "nested summary"
    },
    "single agent response",
    {
      "type": "nested_workflow",
      "responses": [...],
      "finalized_result": "deep nested summary"
    }
  ],
  "finalizedResult": "Overall orchestration summary"
}
```

**Examples**:

**Simple Orchestration**:
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

**Complex Nested Orchestration**:
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

---

### 4. `/autoOrchestrate` - Auto Orchestration Agent
**Method**: `POST`  
**Purpose**: Automatically determine roles and create agent swarms for user commands

**Request**:
```json
{
  "command": "your command here"
}
```

**Response**:
```json
{
  "received_command": "your command here",
  "auto_orchestrate_response": {
    "identified_role": "Research Analyst",
    "m_language_spec": "swarm task_swarm { ... }",
    "swarm_result": {
      "success": true,
      "execution_results": "processed results"
    },
    "processing_steps": [
      "Role identification",
      "M Language specification generation",
      "Swarm execution",
      "Result compilation"
    ]
  },
  "finalizedResult": "Final processed result"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/autoOrchestrate" \
  -H "Content-Type: application/json" \
  -d '{"command": "check what are the best tourist destinations in sri lanka"}'
```

**Features**:
- **Role Identification**: Automatically identifies the most appropriate professional role for the task
- **M Language Generation**: Creates specialized M Language specifications for agent swarms
- **Swarm Execution**: Executes the generated specifications using the MParser runtime
- **Error Handling**: Graceful fallbacks when parsing or execution fails

---

### 5. `/` - Root Endpoint
**Method**: `GET`  
**Purpose**: Health check and API information

**Response**:
```json
{
  "message": "Welcome to FastGraph API with LangGraph Agent"
}
```

---

## Data Types

### TaskItem (Recursive Type)
```python
TaskItem = Union[str, List['TaskItem']]
```

This allows for unlimited nesting levels:
- `"string"` → Single agent
- `["string1", "string2"]` → Simple workflow
- `["string", ["nested1", "nested2"]]` → Nested workflow
- `[["deep", ["deeper", ["deepest"]]]]` → Deep nesting

### Response Types

#### Agent Response
```python
str  # Direct AI response
```

#### Workflow Response
```python
{
  "type": "workflow",
  "responses": List[str],
  "finalized_result": str
}
```

#### Nested Workflow Response
```python
{
  "type": "nested_workflow", 
  "responses": List[Any],
  "finalized_result": str
}
```

---

## Error Handling

### HTTP Status Codes
- `200` - Success
- `422` - Validation error (invalid request structure)
- `500` - Internal server error

### Error Response Format
```json
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "field_name"],
      "msg": "Error message",
      "input": "invalid_input"
    }
  ]
}
```

---

## Configuration

### Environment Variables
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

### Valid Models
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4o`
- `gpt-4o-mini`

---

## Testing

### Integration Tests
```bash
# Run all integration tests
python test/test_orchestrate_integration.py

# Run pytest tests
pytest test/test_orchestrate_pytest.py -v
```

### Test Coverage
- Simple orchestration
- Nested workflows
- Complex nested structures
- Deep nesting (3+ levels)
- Mixed content types
- Edge cases
- Large workflows
- Error handling

---

## Performance Considerations

### Response Times
- Single agent: ~2-5 seconds
- Simple workflow: ~5-15 seconds
- Complex orchestration: ~10-30 seconds

### Concurrent Requests
- Supports multiple concurrent requests
- Each request is processed independently
- No request queuing or blocking

### Memory Usage
- Efficient state management
- Proper cleanup of LLM instances
- Optimized response processing

---

## Best Practices

### 1. Request Structure
- Keep individual tasks concise
- Use meaningful task descriptions
- Structure nested workflows logically

### 2. Error Handling
- Always check response status codes
- Handle validation errors gracefully
- Implement retry logic for transient failures

### 3. Performance
- Batch related tasks together
- Use workflows for sequential dependencies
- Avoid extremely deep nesting (>5 levels)

### 4. Security
- Secure your API key
- Use HTTPS in production
- Implement rate limiting if needed

---

## Migration from Previous Versions

### From Basic Agents
- Use `/ask` for single commands (no change)
- Use `/workflowask` for simple workflows (no change)
- Use `/orchestrate` for complex hierarchical workflows (new)

### Type Safety
- All endpoints use Pydantic validation
- Recursive types support unlimited nesting
- Automatic type conversion and validation

---

*This reference provides a comprehensive guide to all FastGraph API endpoints and their usage.* 