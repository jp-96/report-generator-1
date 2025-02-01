# code/example/fastapi-report-engine/api/endpoints/odt.py

from fastapi import APIRouter, File, UploadFile
from typing import List, Optional
from api.models.render_request import RenderRequest
from services.report_engine import generate_report

router = APIRouter()


@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    return generate_report("odt", request, template, medias)
