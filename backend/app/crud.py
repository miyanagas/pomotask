from sqlalchemy.orm import Session
from . import models, schemas


# toDoListを取得
def get_toDoList(db: Session, done_filter: bool):
    if done_filter:
        return db.query(models.ToDoItem).filter(models.ToDoItem.is_done == False).all()
    else:
        return db.query(models.ToDoItem).all()


# ToDoItemを新規作成
def create_toDoItem(db: Session, toDoItem: schemas.toDoItemCreate):
    db_toDoItem = models.ToDoItem(title=toDoItem.title, is_done=False, time_to_complete=0)
    db.add(db_toDoItem)
    db.commit()
    db.refresh(db_toDoItem)
    return db_toDoItem


def update_toDoItem(db: Session, toDoItem: schemas.toDoItem):
    db_toDoItem = (
        db.query(models.ToDoItem).filter(models.ToDoItem.id == toDoItem.id).first()
    )
    db_toDoItem.is_done = toDoItem.is_done
    db_toDoItem.time_to_complete = toDoItem.time_to_complete
    db.commit()
    return db_toDoItem


# 全てのstock、salesを削除
def delete_toDoItem(db: Session):
    db.query(models.ToDoItem).delete()
    db.commit()
