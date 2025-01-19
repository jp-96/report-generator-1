# odt2.py

import re
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from jinja2 import Template
from starlette.background import BackgroundTask
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from rptgen1.odt_report_generator import ODTReportGenerator, UnoClientConfig

UNOSERVER_HOST = "unoserver"

router = APIRouter()

# Define a base model for JSON validation
class JsonBaseModel(BaseModel):
    """
    A base model for JSON validation.
    """
    @model_validator(mode='before')
    @classmethod
    def validate_json(cls, value):
        """
        Validates JSON input and converts it if necessary.

        Args:
            value (str): The JSON input.

        Returns:
            The validated JSON object.
        """
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value

prohibited_chars_pattern = r'[<>:"/\\|?*]'

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by replacing prohibited characters with underscores.

    Args:
        filename (str): The original filename.

    Returns:
        str: The sanitized filename.
    """
    return re.sub(prohibited_chars_pattern, '_', filename)

class ReportGenerationRequest(JsonBaseModel):
    """
    A model for the report generation request.

    Attributes:
        document_content (dict): The content of the document to be rendered.
        file_basename (str): The basename of the file (excluding the extension) to be used for the generated document.
        convert_to_pdf (bool): Indicates if the document should be converted to a PDF file.
        pdf_filter_options (dict): Options for the PDF export filter to be applied during conversion.
    """
    document_content: dict = Field(default={}, description='The content of the document to be rendered.')
    file_basename: str = Field(default="rendered", description='The basename of the file (excluding the extension) to be used for the generated document.')
    convert_to_pdf: bool = Field(default=False, description='Indicates if the document should be converted to a PDF file.')
    pdf_filter_options: dict = Field(default={}, description='Options for the PDF export filter to be applied during conversion. See this link: https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html')

@router.post("/odt", summary="Render the report.", tags=["Render"])
def render(report_request: ReportGenerationRequest, template: UploadFile, images: Optional[List[UploadFile]] = File(None)):
    """
    Renders the report based on the provided template and images.

    Args:
        report_request (ReportGenerationRequest): The report generation request.
        template (UploadFile): The template file.
        images (Optional[List[UploadFile]]): A list of image files.

    Returns:
        FileResponse: The response containing the generated file.
    """
    images = images or []
    response_file_basename = sanitize_filename(Template(report_request.file_basename).render(report_request.document_content))

    # Initialize the report generator
    report_generator = ODTReportGenerator(
        document_content=report_request.document_content,
        file_basename=report_request.file_basename,
        convert_to_pdf=report_request.convert_to_pdf,
        pdf_filter_options=report_request.pdf_filter_options,
        uno_client_config=UnoClientConfig(server=UNOSERVER_HOST)
    )

    # Save the template file
    report_generator.save_template_file(template.file, template.filename)
    
    # Save the image files
    for image in images:
        report_generator.save_media_file(image.file, image.filename)

    try:
        # Handle the request and generate the report
        file_type, result_file_path = report_generator.handle_request(template.filename)
        background_task = BackgroundTask(report_generator.cleanup_working_directories)

        # Return the generated file response
        if file_type == "pdf":
            return FileResponse(
                path=result_file_path,
                filename=response_file_basename + ".pdf",
                background=background_task
            )
        else:
            return FileResponse(
                path=result_file_path,
                media_type="application/octet-stream",
                filename=response_file_basename + ".odt",
                background=background_task
            )

    except Exception as e:
        return {"message": "An error occurred during processing"}
