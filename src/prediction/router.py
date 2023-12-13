from typing import List
from fastapi import APIRouter
from .services import PredictionService
from .schemas import PlaystoreList, YoutubeList, NewsList

router = APIRouter(
  prefix="/predict",
  tags=["predict"]
)

@router.post("/playstore")
async def playstore_prediction(data: PlaystoreList):
  return PredictionService().playstore_predict(data.data)

@router.post("/youtube")
async def youtube_prediction(data: YoutubeList):
  return PredictionService().youtube_predict(data.data)

@router.post("/news")
async def news_prediction(data: NewsList):
  return PredictionService().news_predict(data.data)