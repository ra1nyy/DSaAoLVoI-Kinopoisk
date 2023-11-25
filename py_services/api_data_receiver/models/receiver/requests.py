from pydantic import BaseModel


class KinopoiskDataRequest(BaseModel):
    kinopoisk_data: list | dict
