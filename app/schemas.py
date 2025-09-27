from sqlmodel import SQLModel, Field

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

# Task model to use when creating or updating tasks
class TaskIn(TaskBase):
    pass