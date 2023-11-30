import json

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from models.receiver.requests import KinopoiskDataRequest
from services import ReceiveDataService

receive_data_router = APIRouter(
    prefix='/receive_data'
)


@receive_data_router.post("/",)
async def extract_data(movie: dict):
    service = ReceiveDataService()
    await service.send_to_rabbitmq(movie)

    return status.HTTP_200_OK
