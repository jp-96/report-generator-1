# code/example/fastapi-report-engine/api/endpoints/docx.py

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import List, Optional
from rptgen1 import DOCXReportGenerator, UnoClientConfig
from ..models.docx_request import DOCXRequest
from config import get_settings

settings = get_settings()
uno_client_config = UnoClientConfig(
    server=settings.unoserver_host,
    port=settings.unoserver_port,
    host_location=settings.unoserver_location,
)

router = APIRouter()


@router.post("/docx", summary="Render the report.", tags=["Render"])
def render(
    docx_request: DOCXRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    report_generator = DOCXReportGenerator(
        file_basename=docx_request.file_basename,
        convert_to_pdf=docx_request.convert_to_pdf,
        pdf_filter_options=docx_request.pdf_filter_options,
        uno_client_config=uno_client_config,
    )
    report_generator.save_template_file(template.file, template.filename)
    medias = medias or []
    for f in medias:
        report_generator.save_media_file(f.file, f.filename)
    generated = report_generator.render(
        docx_request.context, docx_request.image_mapping
    )
    return FileResponse(
        path=generated.file_path,
        # Set media_type to 'application/octet-stream' to ensure the file is downloaded as binary data.
        media_type=(
            generated.mime_type
            if docx_request.convert_to_pdf
            else "application/octet-stream"
        ),
        filename=generated.file_name,
        background=BackgroundTask(report_generator.cleanup_working_directories),
    )
