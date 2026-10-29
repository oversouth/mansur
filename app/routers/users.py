from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.models import CreateUserDto, UserDto
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserDto, status_code=201)
def create_user(dto: CreateUserDto, db: Session = Depends(get_db)):
    if user_service.get_user_by_username(db, dto.username):
        raise HTTPException(status_code=400, detail="username already exists")
    return user_service.create_user(db, dto)


@router.get("/", response_model=list[UserDto])
def list_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}", response_model=UserDto)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserDto.model_validate(user)


@router.get("/by-username/{username}", response_model=UserDto)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserDto.model_validate(user)
