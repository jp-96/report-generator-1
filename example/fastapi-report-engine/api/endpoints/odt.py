# code/example/fastapi-report-engine/api/endpoints/odt.py

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import List, Optional
from rptgen1 import ODTReportGenerator, UnoClientConfig
from ..models.odt_request import ODTRequest
from config import get_settings

settings = get_settings()
uno_client_config = UnoClientConfig(
    server=settings.unoserver_host,
    port=settings.unoserver_port,
    host_location=settings.unoserver_location,
)

router = APIRouter()


@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(
    odt_request: ODTRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    report_generator = ODTReportGenerator(
        file_basename=odt_request.file_basename,
        convert_to_pdf=odt_request.convert_to_pdf,
        pdf_filter_options=odt_request.pdf_filter_options,
        uno_client_config=uno_client_config,
    )
    report_generator.save_template_file(template.file, template.filename)
    medias = medias or []
    for f in medias:
        report_generator.save_media_file(f.file, f.filename)
    generated = report_generator.render(odt_request.context)
    return FileResponse(
        path=generated.file_path,
        # Set media_type to 'application/octet-stream' to ensure the file is downloaded as binary data.
        media_type=(
            generated.mime_type
            if odt_request.convert_to_pdf
            else "application/octet-stream"
        ),
        filename=generated.file_name,
        background=BackgroundTask(report_generator.cleanup_working_directories),
    )
