from pydantic import BaseSettings


class Config(BaseSettings):
    RECEIVER_URL: str
    KINOPOISK_API_TOKEN: str

    class Config:
        env_file = ".env"
        frozen = True
