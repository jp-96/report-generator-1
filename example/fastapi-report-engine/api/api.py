from fastapi import APIRouter
from .endpoints import odt

api_router = APIRouter()
api_router.include_router(odt.router, tags=["Render"])
