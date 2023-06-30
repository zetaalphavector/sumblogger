from fastapi import FastAPI
from zav.api import setup_api

from src.bootstrap import bootstrap
from src.controllers import routers

app = FastAPI()

setup_api(app=app, bootstrap=bootstrap, routers=routers)


@app.get("/healthcheck")
async def read_main():
    return {"status": "ok"}
