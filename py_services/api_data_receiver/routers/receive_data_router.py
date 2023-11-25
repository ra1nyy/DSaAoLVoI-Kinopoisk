from fastapi import APIRouter
from starlette import status

from models.receiver.requests import KinopoiskDataRequest
from services import ReceiveDataService

receive_data_router = APIRouter(
    prefix='/receive_data'
)


@receive_data_router.post("/",)
async def extract_data(body: KinopoiskDataRequest):
    service = ReceiveDataService()
    await service.send_to_rabbitmq(body.kinopoisk_data)

    return status.HTTP_200_OK
