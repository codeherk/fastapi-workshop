from fastapi import FastAPI, HTTPException
from .schemas import Task, TaskIn
from . import storage

app = FastAPI(title="Tasks API")

@app.post("/tasks", response_model=Task, status_code=201)
def create(task: TaskIn):
    return storage.create_task(task)

@app.get("/tasks", response_model=list[Task])
def list_all():
    return storage.list_tasks()

@app.get("/tasks/{tid}", response_model=Task)
def get_one(tid: int):
    t = storage.get_task(tid)
    if not t:
        raise HTTPException(404, detail="Not found")
    return t

@app.put("/tasks/{tid}", response_model=Task)
def update(tid: int, task: TaskIn):
    t = storage.update_task(tid, task)
    if not t:
        raise HTTPException(404, detail="Not found")
    return t

@app.delete("/tasks/{tid}", status_code=204)
def delete(tid: int):
    if not storage.delete_task(tid):
        raise HTTPException(404, detail="Not found")