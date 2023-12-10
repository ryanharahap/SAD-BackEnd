from typing import Union
from uuid import UUID
from pydantic import BaseModel

class UserBase(BaseModel):
  email: str
  name: str
  password: str

class UserCreate(UserBase):
  pass

class UserLogin(BaseModel):
  email: str
  password: str

class UserReponse(BaseModel):
  token: str

class User(UserBase):
  id: UUID

  class Config:
    orm_mode = True