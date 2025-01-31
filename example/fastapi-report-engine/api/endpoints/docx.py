# code/example/fastapi-report-engine/api/endpoints/docx.py

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import List, Optional
from rptgen1 import DOCXReportGenerator
from api.models.render_request import RenderRequest
from config import get_uno_client_config

router = APIRouter()


@router.post("/docx", summary="Render the report.", tags=["Render"])
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    generator = DOCXReportGenerator(
        file_basename=request.file_basename,
        convert_to_pdf=request.convert_to_pdf,
        pdf_filter_options=request.pdf_filter_options,
        uno_client_config=get_uno_client_config(),
    )
    try:
        generator.save_template_file(template.file, template.filename)
        medias = medias or []
        for f in medias:
            generator.save_media_file(f.file, f.filename)
        rendered = generator.render(request.context)
        return FileResponse(
            path=rendered.file_path,
            media_type=rendered.mime_type,
            filename=rendered.file_name,
            background=BackgroundTask(generator.cleanup_working_directories),
        )
    except Exception as e:
        generator.cleanup_working_directories()
        raise e
