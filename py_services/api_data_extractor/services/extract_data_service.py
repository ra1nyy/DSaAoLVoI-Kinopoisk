from settings.config import Config

from kinopoisk_dev import KinopoiskDev
from kinopoisk_dev.model import Movie
from fastapi.exceptions import HTTPException
import aiohttp


class ExtractDataService:
    def __init__(self):
        self.kp_api_access = KinopoiskDev(token="ACBSC0V-ST9M9MQ-P63YSZN-8CG8B2N")
        self.config = Config()

    async def extract_data(self):
        movie: Movie = await self.kp_api_access.arandom()
        return movie
        #await self._send_data_to_receiver(movie.dict())

    async def _send_data_to_receiver(self, data: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.config.RECEIVER_URL) as response:
                if response.status != 200:
                    raise HTTPException(
                        403,
                        f"Response from receiver not 200: {response.status}",
                    )
