from fastapi import APIRouter
from kinopoisk_dev.model import Movie

from services.extract_data_service import ExtractDataService

extract_data_router = APIRouter(
    prefix='/extract_data'
)


@extract_data_router.post(
    "/",
    response_model=Movie,
    responses={403: {'description': 'external API access error'}},
)
async def extract_data():
    service = ExtractDataService()  # TODO: change to DI
    return await service.extract_data()
