from fastapi import FastAPI, HTTPException
from .schemas import TaskPublic, TaskCreate, TaskUpdate, TaskWithAIResponse
from .service import Service

service = Service()
app = FastAPI(title="Tasks API")

@app.post("/tasks", response_model=TaskWithAIResponse, status_code=201)
def create(task: TaskCreate):
    return service.create_task_with_ai_response(task)

@app.get("/tasks", response_model=list[TaskPublic])
def list_all():
    return service.storage.list_tasks()

@app.get("/tasks/{tid}", response_model=TaskPublic)
def get_one(tid: int):
    try: 
        t = service.storage.get_task(tid)
        return t
    except Exception as e:
        raise HTTPException(404, detail=str(e))

@app.patch("/tasks/{tid}", response_model=TaskPublic)
def update(tid: int, task: TaskUpdate):
    try: 
        t = service.storage.update_task(tid, task)
        return t
    except Exception as e:
        raise HTTPException(404, detail=str(e))

@app.delete("/tasks/{tid}", status_code=204)
def delete(tid: int):
    try: 
        service.storage.delete_task(tid)
    except Exception as e:
        raise HTTPException(404, detail=str(e))