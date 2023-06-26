from fastapi import APIRouter

from src.controllers import v1

routers = [
    ("/v1", router) for router in v1.__dict__.values() if isinstance(router, APIRouter)
]
