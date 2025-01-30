# code/example/fastapi-report-engine/api/models/odt_request.py

from pydantic import Field
from ._request_base_model import RequestBaseModel


class ODTRequest(RequestBaseModel):
    context: dict = Field(default={})
