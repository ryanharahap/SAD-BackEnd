from fastapi import APIRouter
from .services import PredictionService
from .schemas import InputList

router = APIRouter(
  prefix="/predict",
  tags=["predict"]
)

@router.post("/playstore")
async def playstore_prediction(data: InputList):
  return PredictionService().playstore_predict(data)

@router.post("/youtube")
async def youtube_prediction(data: InputList):
  return PredictionService().youtube_predict(data)

@router.post("/news")
async def news_prediction(data: InputList):
  return PredictionService().news_predict(data)