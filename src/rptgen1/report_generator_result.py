# code/src/rptgen1/report_generator_result.py

import re
from typing import NamedTuple
from jinja2 import Template


def render_file_basename(file_basename: str, context: dict) -> str:
    rendered_file_basename = Template(file_basename).render(context)
    return re.sub(r'[<>:"/\\|?*\r\n\t]', "_", rendered_file_basename)


class ReportGeneratorResult(NamedTuple):
    file_path: str
    mime_type: str
    file_name: str
