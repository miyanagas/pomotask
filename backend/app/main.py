from typing import Annotated
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, delete
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_session, create_db_and_tables, drop_db_and_tables
from app.models import Todo, TodoCreate, TodoPublic, TodoUpdate


app = FastAPI()

# CORSの設定
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
def on_shutdown():
    drop_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# ToDoItemを新規作成するリクエスト
@app.post("/todo-list/", response_model=TodoPublic)
def create_todo(todo: TodoCreate, session: SessionDep):
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


# ToDoItemを更新するリクエスト
@app.put("/todo-list/{id}", response_model=TodoPublic)
def update_todo(id: uuid.UUID, todo: TodoUpdate, session: SessionDep):
    db_todo = session.get(Todo, id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# ToDoListを取得するリクエスト
@app.get("/todo-list/", response_model=list[TodoPublic])
def read_todo_list(session: SessionDep, filter: bool = False):
    if filter:
        db_todo_list = session.exec(select(Todo).where(Todo.is_done == False)).all()
    else:
        db_todo_list = session.exec(select(Todo)).all()
    return db_todo_list

# ToDoItemを取得するリクエスト
@app.get("/todo-list/{id}", response_model=TodoPublic)
def read_todo(id: uuid.UUID, session: SessionDep):
    db_todo = session.get(Todo, id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# ToDoListを削除するリクエスト
@app.delete("/todo-list/")
def delete_todo_list(session: SessionDep):
    session.exec(delete(Todo))
    session.commit()
    return {"ok": True}
