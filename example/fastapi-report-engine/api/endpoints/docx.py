# code/example/fastapi-report-engine/api/endpoints/docx.py

from fastapi import APIRouter, File, UploadFile
from typing import List, Optional
from api.models.render_request import RenderRequest
from services.report_engine import generate_report

router = APIRouter()


@router.post("/docx", summary="Render the report.", tags=["Render"])
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    return generate_report("docx", request, template, medias)
