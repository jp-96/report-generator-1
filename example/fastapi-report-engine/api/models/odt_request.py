
from pydantic import BaseModel, Field, model_validator

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

class ODTRequest(JsonBaseModel):
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
