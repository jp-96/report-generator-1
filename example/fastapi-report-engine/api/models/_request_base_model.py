# example\fastapi-report-engine\api\models\_request_base_model.py

from pydantic import Field
from ._json_base_model import JsonBaseModel


class RequestBaseModel(JsonBaseModel):
    file_basename: str = Field(default="rendered")
    convert_to_pdf: bool = Field(default=False)
    pdf_filter_options: dict = Field(
        default={}
    )  # See this link: https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html
