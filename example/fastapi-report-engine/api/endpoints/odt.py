# code/example/fastapi-report-engine/api/endpoints/odt.py

from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
from typing import List, Optional
from rptgen1 import ODTReportGenerator, UnoClientConfig
from ..models.odt_request import ODTRequest

UNOSERVER_HOST = "unoserver"
uno_client_config=UnoClientConfig(server=UNOSERVER_HOST)

router = APIRouter()

@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(odt_request: ODTRequest, template: UploadFile, medias: Optional[List[UploadFile]] = File(None)):
    """
    Renders the report based on the provided template and medias.

    Args:
        - odt_request (ReportGenerationRequest): The report generation request.
        - template (UploadFile): The template file.
        - medias (Optional[List[UploadFile]]): A list of image files.

    Returns:
        - FileResponse: The response containing the generated file.
    """
    try:
        medias = medias or []

        # Initialize the report generator
        report_generator = ODTReportGenerator(
            document_content=odt_request.document_content,
            file_basename=odt_request.file_basename,
            convert_to_pdf=odt_request.convert_to_pdf,
            pdf_filter_options=odt_request.pdf_filter_options,
            uno_client_config=uno_client_config
        )

        # Save the template file
        report_generator.save_template_file(template.file, template.filename)
        
        # Save the image files
        for f in medias:
            report_generator.save_media_file(f.file, f.filename)

        # Handle the request and generate the report
        result_file_path, media_type, rendered_filename = report_generator.handle_request(template.filename)
        background_task = BackgroundTask(report_generator.cleanup_working_directories)

        # Return the generated file response
        return FileResponse(
            path=result_file_path,
            media_type=media_type,
            filename=rendered_filename,
            background=background_task
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "An error occurred during processing"},
        )
