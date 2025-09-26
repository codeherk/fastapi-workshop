from .schemas import Task, TaskIn

_db = {}
_counter = 0

def create_task(data: TaskIn) -> Task:
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