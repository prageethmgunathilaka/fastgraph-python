# FastGraph Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.8+
- OpenAI API key
- Git (optional)

### 2. Installation

```bash
# Clone the repository (if using Git)
git clone <repository-url>
cd fatgraph

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

#### Option A: Environment Variables
```bash
# Set environment variables
export OPENAI_API_KEY="your-openai-api-key-here"
export DEFAULT_LLM_MODEL="gpt-3.5-turbo"
export LLM_TEMPERATURE="0.7"
export HOST="0.0.0.0"
export PORT="8000"
```

#### Option B: .env File
```bash
# Copy the template
cp env_template.txt .env

# Edit the .env file with your settings
# Replace 'your-openai-api-key-here' with your actual OpenAI API key
```

### 4. Run the Server

```bash
# Start the FastAPI server
python main.py
```

The server will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

---

## Project Structure

```
fatgraph/
├── agents/                 # Agent implementations
│   ├── __init__.py        # Package exports
│   ├── regular_agent.py   # Single command agent
│   ├── workflow_agent.py  # Multi-command workflow agent
│   ├── orchestrate_agent.py # Hierarchical orchestration agent
│   └── MParser/           # Specialized parsing module
├── config.py              # Configuration management
├── main.py                # FastAPI application
├── requirements.txt       # Dependencies
├── env_template.txt       # Environment template
├── docs/                  # Documentation
│   ├── IMPROVEMENTS.md   # Project improvements
│   ├── API_REFERENCE.md  # API documentation
│   └── SETUP_GUIDE.md    # This file
├── test/                  # Test suite
│   ├── test_ask_endpoint.py
│   ├── test_workflow_endpoint.py
│   ├── test_workflow_integration.py
│   ├── test_orchestrate_endpoint.py
│   ├── test_orchestrate_integration.py
│   └── test_orchestrate_pytest.py
└── README.md
```

---

## Testing

### Run All Tests
```bash
# Integration tests
python test/test_orchestrate_integration.py

# Pytest tests
pytest test/test_orchestrate_pytest.py -v

# All tests
pytest test/ -v
```

### Test Individual Endpoints
```bash
# Test /ask endpoint
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'

# Test /workflowask endpoint
curl -X POST "http://localhost:8000/workflowask" \
  -H "Content-Type: application/json" \
  -d '{"commands": ["Task 1", "Task 2", "Task 3"]}'

# Test /orchestrate endpoint
curl -X POST "http://localhost:8000/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{"tasks": [["Hello"], ["World"]]}'
```

---

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `DEFAULT_LLM_MODEL` | `gpt-3.5-turbo` | LLM model to use |
| `LLM_TEMPERATURE` | `0.7` | Model temperature (0.0-1.0) |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

### Valid Models
- `gpt-3.5-turbo` (recommended for cost)
- `gpt-4` (better quality)
- `gpt-4-turbo` (balanced)
- `gpt-4o` (latest)
- `gpt-4o-mini` (fastest)

---

## Troubleshooting

### Common Issues

#### 1. "OPENAI_API_KEY is required"
**Solution**: Set your OpenAI API key in environment variables or .env file

#### 2. "invalid model ID" error
**Solution**: Use a valid model from the list above

#### 3. "Connection refused" error
**Solution**: Check if the server is running on the correct port

#### 4. Import errors
**Solution**: Install dependencies with `pip install -r requirements.txt`

#### 5. Validation errors
**Solution**: Check request format in API documentation

### Debug Mode

Enable debug logging:
```python
# In config.py or environment
LOG_LEVEL = "DEBUG"
```

### Health Check

Test server connectivity:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"message": "Welcome to FastGraph API with LangGraph Agent"}
```

---

## Development

### Adding New Agents

1. Create agent file in `agents/` directory
2. Implement required functions
3. Update `agents/__init__.py` exports
4. Add tests in `test/` directory

### Adding New Endpoints

1. Add endpoint in `main.py`
2. Define request/response models
3. Implement business logic
4. Add comprehensive tests

### Code Style

- Use type hints
- Follow PEP 8
- Add docstrings
- Write tests for new features

---

## Production Deployment

### Environment Setup
```bash
# Production environment variables
export OPENAI_API_KEY="your-production-api-key"
export DEFAULT_LLM_MODEL="gpt-4"
export HOST="0.0.0.0"
export PORT="8000"
export LOG_LEVEL="INFO"
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

---

## Support

### Documentation
- `docs/IMPROVEMENTS.md` - Project improvements and features
- `docs/API_REFERENCE.md` - Complete API documentation
- `README.md` - Project overview

### Testing
- Run integration tests to verify functionality
- Check API documentation for endpoint usage
- Use interactive docs at `/docs` endpoint

### Issues
- Check troubleshooting section above
- Verify configuration settings
- Test with simple requests first

---

*This guide provides everything needed to set up and run the FastGraph project.* 