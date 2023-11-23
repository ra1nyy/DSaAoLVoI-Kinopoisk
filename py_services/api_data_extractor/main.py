import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from routers.extract_data_router import extract_data_router
from docs.custom_openapi import docs_router

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract_data_router)
docs_router(app)

@app.get('/')
def index():
    return {'message': 'Everything online'}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=3001,
    )
