from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    QUEUE_NAME: str
    RABBIT_URL: str

    class Config:
        env_file = ".env"
        frozen = True
