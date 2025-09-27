from sqlmodel import SQLModel, Field
from pydantic import BaseModel

# Fields shared by all Task models
class TaskBase(SQLModel):
    title: str = Field(..., min_length=1, max_length=120)
    done: bool = False

# Task table model. This will be the model used in the database tables
class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Task model to return to clients  
class TaskPublic(TaskBase):
    id: int

# Task model to use when creating tasks
class TaskCreate(TaskBase):
    pass

# Task model to use when updating tasks
class TaskUpdate(TaskBase):
    title: str | None = None
    done: bool | None = None

# Model for the AI-generated follow-up suggestion (not stored in DB)
class TaskWithAIResponse(BaseModel):
    task: TaskPublic
    model_response: str | None
