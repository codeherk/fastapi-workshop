# FastAPI Workshop

## Requirements
- Python 3.10+

## Setup
Install dependencies:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "fastapi[standard]" uvicorn pydantic
```

# Run the application
```bash
uvicorn app.main:app --reload
```

## Test Endpoints
**Create**
```bash
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"win hackathon"}'
```

**List**
```bash
curl http://127.0.0.1:8000/tasks
```

**Update**
```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"title":"ship MVP","done":true}'
```

**Delete**
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 -i
```

## API Documentation
Visit `http://localhost:8000/docs` for the interactive API documentation.