from fastapi import FastAPI
from zav.api import setup_api

from src.bootstrap import bootstrap
from src.controllers import routers
from src.dependencies import (
    get_pass_through_text_completion_service,
    pass_through_text_completion_service_dependency,
)

app = FastAPI()
app.dependency_overrides[
    get_pass_through_text_completion_service
] = pass_through_text_completion_service_dependency

setup_api(app=app, bootstrap=bootstrap, routers=routers)


@app.get("/healthcheck")
async def read_main():
    return {"status": "ok"}
