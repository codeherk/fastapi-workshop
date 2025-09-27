from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from .schemas import TaskPublic, TaskIn
from .storage import Storage
from .service import service


app = FastAPI(title="Tasks API")

@app.post("/tasks", response_model=TaskPublic, status_code=201)
def create(task: TaskIn):
    return service.storage.create_task(task)

@app.get("/tasks", response_model=list[TaskPublic])
def list_all():
    return service.storage.list_tasks()

@app.get("/tasks/{tid}", response_model=TaskPublic)
def get_one(tid: int):
    t = service.storage.get_task(tid)
    # if not t:
    #     raise HTTPException(404, detail="Not found")
    return t

@app.put("/tasks/{tid}", response_model=TaskPublic)
def update(tid: int, task: TaskIn):
    t = service.storage.update_task(tid, task)
    # if not t:
    #     raise HTTPException(404, detail="Not found")
    return t

@app.delete("/tasks/{tid}", status_code=204)
def delete(tid: int):
    return service.storage.delete_task(tid)
    # if not service.storage.delete_task(tid):
        # raise HTTPException(404, detail="Not found")