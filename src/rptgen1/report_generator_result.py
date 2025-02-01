# code/src/rptgen1/report_generator_result.py

from typing import NamedTuple


class ReportGeneratorResult(NamedTuple):
    filename: str
    mime_type: str
    file_path: str
