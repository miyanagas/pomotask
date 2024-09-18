from pydantic import BaseModel


# ToDoItem schema
class toDoItemCreate(BaseModel):
    title: str


class toDoItem(toDoItemCreate):
    id: int
    is_done: bool
