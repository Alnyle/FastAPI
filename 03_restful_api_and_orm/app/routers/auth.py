from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users
from starlette import status
from database import SessionLocal
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Think of it a password hashing manager.
# It lets you:
#   - Define which hashing algorithms to use.
#   - Verify passwords against stored hashes.
#   - Automatically upgrade old hashes to newer algorithms if needed.

# "schemes" is a list of hashing algorithms that the context will use.
# "bcrypt" is one of the secure algorithms available in Passlib.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_db():
    
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]




class CreateUserRequest(BaseModel):
    
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str



@router.get('/auth', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
     
    return db.query(Users).all()


@router.get('/auth/{id}', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, id: int):
    
    
    user = db.query(Users).filter(Users.id == id).first()
    
    if user is not None:
        return user
    
    raise HTTPException(status_code=404, detail="User not found.")


@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )
    
    db.add(create_user_model)
    db.commit()
    return create_user_model
     
     
@router.post('/token')
async def login_for_access_token():
    return "token"