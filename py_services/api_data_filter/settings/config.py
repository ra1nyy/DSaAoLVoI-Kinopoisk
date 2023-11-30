from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    QUEUE_NAME: str
    ELASTIC_QUEUE_NAME: str
    RABBIT_URL: str
    JSON_FILE: str
    OUTPUT_JSON_FILE: str

    class Config:
        env_file = ".env"
        frozen = True
