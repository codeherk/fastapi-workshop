from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, 
from sqlalchemy import Engine
from .schemas import Task, TaskIn

engine: Engine
# SessionDep: Session = Session()

def initialize(sqlite_url: str, connect_args):
    # Create engine
    global engine, SessionDep
    engine = create_engine(sqlite_url, connect_args=connect_args)

    # Create database and tables
    create_db_and_tables()
    # Set session annotation
    # SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_task(data: TaskIn, session: SessionDep) -> Task:
    global _counter
    _counter += 1
    t = Task(id=_counter, **data.model_dump())
    _db[t.id] = t
    return t

def list_tasks(): return list(_db.values())

def get_task(tid: int): return _db.get(tid)

def update_task(tid: int, data: TaskIn):
    if tid not in _db: return None
    t = Task(id=tid, **data.model_dump())
    _db[tid] = t
    return t

def delete_task(tid: int): return _db.pop(tid, None) is not None