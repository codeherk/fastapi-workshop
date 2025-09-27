from typing import Annotated

from fastapi import Query
from sqlmodel import Session, SQLModel, create_engine, select
from .schemas import Task, TaskCreate, TaskUpdate

class Storage:
    def __init__(self, db_url, connect_args):
        self.engine = create_engine(db_url, connect_args=connect_args)
        self.create_db_and_tables()
        self.session = Session(self.engine)
        return

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def create_task(self, data: TaskCreate) -> Task:
        db_task = Task.model_validate(data)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def list_tasks(self, limit: Annotated[int, Query(le=100)] = 100): return self.session.exec(select(Task).offset(0).limit(limit)).all()

    def get_task(self, tid: int): 
        task = self.session.get(Task, tid)
        if not task:
            raise Exception("Task not found")
        return task

    def update_task(self, tid: int, data: TaskUpdate):
        task = self.session.get(Task, tid)
        if not task:
            raise Exception("Task not found")
        task_data = data.model_dump(exclude_unset=True)
        task.sqlmodel_update(task_data)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, tid: int):
        task = self.session.get(Task, tid)
        if not task:
            raise Exception("Task not found")
        self.session.delete(task)
        self.session.commit()
        return {"ok": True}