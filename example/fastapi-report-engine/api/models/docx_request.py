# code/example/fastapi-report-engine/api/models/odt_request.py

from pydantic import Field
from ._request_base_model import RequestBaseModel


class DOCXRequest(RequestBaseModel):
    context: dict = Field(default={})
    image_mapping: dict = Field(default={})
