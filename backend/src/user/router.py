from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from .services import UserService
from . import schemas
from ..utils.get_db import get_db
from typing import Union
from typing_extensions import Annotated

router = APIRouter(
  prefix="/user",
  tags=["user"]
)

@router.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
  return UserService(db).register(user)

@router.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
  return UserService(db).login(user)
