from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine

# Routes
from .user import router as user_router
from .prediction import router as predict_router

# Models
from .models import users

users.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(user_router.router)
app.include_router(predict_router.router)

@app.get('/')
def check_status():
  return {
    "status": "Healthy"
  }