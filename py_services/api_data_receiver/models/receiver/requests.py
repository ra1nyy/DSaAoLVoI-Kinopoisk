from typing import Any

from pydantic import BaseModel


class KinopoiskDataRequest(BaseModel):
    data: Any
