import datetime

from settings.config import Config

from kinopoisk_dev import KinopoiskDev, MovieField, MovieParams
import json
from datetime import datetime, date
import requests


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class ExtractDataService:
    def __init__(self):
        self.config = Config()
        self.kp_api_access = KinopoiskDev(token=self.config.KINOPOISK_API_TOKEN)

    async def extract_data(self):
        movies = await self.kp_api_access.afind_many_movie(params=[
            MovieParams(keys=MovieField.PAGE, value="1"),
            MovieParams(keys=MovieField.LIMIT, value="2000"),
        ])
        await self._send_data_to_receiver(movies.dict())

        return movies

    async def _send_data_to_receiver(self, data):
        requests.post(self.config.RECEIVER_URL, data=json.dumps(data, default=json_serial))
