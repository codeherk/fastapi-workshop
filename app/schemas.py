from pydantic import BaseModel, Field

class TaskIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    done: bool = False

class Task(TaskIn):
    id: int