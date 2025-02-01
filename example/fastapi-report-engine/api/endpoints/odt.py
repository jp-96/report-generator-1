# code/example/fastapi-report-engine/api/endpoints/odt.py

from fastapi import APIRouter, File, UploadFile
from typing import List, Optional
from api.models.render_request import RenderRequest
from report_engine import generate_report

router = APIRouter()


@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    response = generate_report("odt", request, template, medias)
    if request.convert_to_pdf:
        # Set media_type to 'application/octet-stream' to ensure the file is downloaded as binary data.
        response.media_type = "application/octet-stream"
    return response
