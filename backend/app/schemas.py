from pydantic import BaseModel


# ToDoItem schema
class toDoItemCreate(BaseModel):
    title: str

class toDoItemUpdate(BaseModel):
    is_done: bool | None = None
    time_to_complete: int | None = None

class toDoItem(toDoItemCreate):
    id: int
    is_done: bool
    time_to_complete: int
