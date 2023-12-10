from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas
from .repositories import UserRepo
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..config import Settings
from ..utils.error_response import error_response

class UserService:
  def __init__(self, db: Session):
    self.repository = UserRepo(db)
    self.settings = Settings()
    self.pwd_context = CryptContext(schemes=["bcrypt"])

  def __password_hash(self, password: str):
    return self.pwd_context.hash(password)
  
  def __verify_password(self, password: str, hashed_password: str):
    return self.pwd_context.verify(password, hashed_password)
  
  def __generate_token(self, email: str, name: str):
    to_encode = {
      "email": email,
      "name": name
    }
    encoded_jwt = jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)
    return encoded_jwt

  def login(self, login: schemas.UserLogin):
    user = self.repository.find_by_email(login.email)

    if not user:
      raise HTTPException(400, detail=error_response('user does not exist'))
    
    if not self.__verify_password(login.password, user.password):
      raise HTTPException(400, detail=error_response('incorrect password'))
    
    token = self.__generate_token(user.email, user.name)
    
    return {
      "access_token": token
    }

  def register(self, user: schemas.UserCreate):
    user_exist = self.repository.find_by_email(user.email)

    if user_exist:
      raise HTTPException(400, detail=error_response(f"user with email ${user.email} already exist"))

    hashed_password = self.__password_hash(user.password)

    new_user = schemas.UserCreate(
      email=user.email,
      name=user.name,
      password=hashed_password
    )

    created_user = self.repository.create(new_user)

    token = self.__generate_token(created_user.email, created_user.name)

    return {
      "access_token": token
    }