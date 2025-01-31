# code/example/fastapi-report-engine/api/endpoints/odt.py

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from typing import List, Optional
from rptgen1 import ODTReportGenerator
from api.models.render_request import RenderRequest
from config import get_uno_client_config

router = APIRouter()


@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    generator = ODTReportGenerator(
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
            # Set media_type to 'application/octet-stream' to ensure the file is downloaded as binary data.
            media_type=(
                rendered.mime_type
                if request.convert_to_pdf
                else "application/octet-stream"
            ),
            filename=rendered.file_name,
            background=BackgroundTask(generator.cleanup_working_directories),
        )
    except Exception as e:
        generator.cleanup_working_directories()
        raise e
