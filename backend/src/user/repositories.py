from uuid import UUID
from sqlalchemy.orm import Session
from ..models import users as models
from . import schemas

class UserRepo:
  def __init__(self, db: Session):
    self.db = db

  def find_all(self):
    return self.db.query(models.User).all()

  def find_by_email(self, email: str):
    return self.db.query(models.User).filter(models.User.email == email).first()
  
  def create(self, user: schemas.UserCreate):
    new_user = models.User(
      email=user.email,
      name=user.name,
      password=user.password
    )
    self.db.add(new_user)
    self.db.commit()
    self.db.refresh(new_user)
    return new_user
