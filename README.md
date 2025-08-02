# FastGraph

A simple FastAPI application.

## Installation

```bash
pip install -r requirements.txt
```

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
- `GET /ask` - Returns "hello world"

## Access the API

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc 