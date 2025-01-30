# code/example/fastapi-report-engine/api/api.py

from fastapi import APIRouter
from .endpoints import odt, docx

api_router = APIRouter()
api_router.include_router(odt.router, tags=["Render"])
api_router.include_router(docx.router, tags=["Render"])
