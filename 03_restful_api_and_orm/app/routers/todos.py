from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter()


def get_db():
    
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()



# dependency Injection: mean we nedd to do somthing before we execute what we are trying to execute
# that will allow us to be able to do some kind of code behind of the scences and then inject the dependencies


# db: Annotated[Session, Depends(get_db)]
# Depends(get_db) → tells FastAPI: “Before calling this route, run get_db() and inject its return value into db.”
# Annotated[Session, ...] → says "db is a SQLAlchemy Session object, provided by this dependency." 
db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency):
    return db.query(Todos).all()


@router.get('/todo/{id}', status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail="Todo not found.")



@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    
    todo_model = Todos(**todo_request.model_dump()) # Generate a dictionary representation of the model
    
    db.add(todo_model) # staging the change to the database (preparing the transaction to the database )
    db.commit() # apply the change to the database (execute the transaction)
    

@router.put('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
 


@router.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, id: int = Path(gt=0)):
    
    todo = db.query(Todos).filter(Todos.id == id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()

# {
#   "title": "Watch golab tutorial",
#   "description": "learn to use golab power from GPU and RAM",
#   "priority": 2,
#   "complete": False
# }