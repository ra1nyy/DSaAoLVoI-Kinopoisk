import logging
import random
import string
import time
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from dotenv import load_dotenv

from routers.receive_data_router import receive_data_router

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI()
# app.include_router(api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def index():
    return {'message': 'Everything online'}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware for log requests and their answers
    :param request:
    :param call_next:
    :return:
    """
    idem = f"{random.choices(string.ascii_uppercase)}      {string.digits}"
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="DSaAolVol-Kinopoisk API DATA RECEIVER",
        version="0.1",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.include_router(receive_data_router)
# docs_router(app)

app.openapi = custom_openapi
