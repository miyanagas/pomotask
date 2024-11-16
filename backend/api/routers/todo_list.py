from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, delete

import uuid

from api.models.todo import Todo, TodoCreate, TodoPublic, TodoUpdate
from api.auth import UserDep
from api.database import SessionDep

router = APIRouter(prefix="/todo-list", tags=["todo-list"])

# Todo新規作成リクエスト
@router.post("/", response_model=TodoPublic)
def create_todo(todo: TodoCreate, user: UserDep, session: SessionDep):
    todo_data = todo.model_dump()
    todo_data["user_id"] = user.id
    db_todo = Todo.model_validate(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# Todo更新リクエスト
@router.put("/{id}", response_model=TodoPublic)
def update_todo(id: uuid.UUID, todo: TodoUpdate, user: UserDep, session: SessionDep):
    db_todo = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.id == id)).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# Todo一覧取得リクエスト
@router.get("/", response_model=list[TodoPublic])
def read_todo_list(user: UserDep, session: SessionDep, filter: bool = False):
    if filter:
        db_todo_list = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.is_done == False)).all()
    else:
        db_todo_list = session.exec(select(Todo).where(Todo.user_id == user.id)).all()
    return db_todo_list

# Todo取得リクエスト
@router.get("/{id}", response_model=TodoPublic)
def read_todo(id: uuid.UUID, user: UserDep, session: SessionDep):
    db_todo = session.exec(select(Todo).where(Todo.user_id == user.id).where(Todo.id == id)).first()
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return db_todo

# Todo全削除リクエスト
@router.delete("/")
def delete_todo_list(user: UserDep, session: SessionDep):
    session.exec(delete(Todo).where(Todo.user_id == user.id))
    session.commit()
    return {"ok": True}