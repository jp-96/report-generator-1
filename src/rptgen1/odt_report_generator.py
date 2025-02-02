# code/src/rptgen1/odt_report_generator.py

import os
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult
from .base_report_generator import BaseReportGenerator


class ODTReportGenerator(BaseReportGenerator):
    def __init__(
        self,
        file_basename: str,
        convert_to_pdf: bool,
        pdf_filter_options: dict,
        uno_client_config: UnoClientConfig,
    ):
        super().__init__(
            file_basename, convert_to_pdf, pdf_filter_options, uno_client_config
        )

    def _render(self, context: dict) -> ReportGeneratorResult:
        filename = self.rendered_file_basename + ".odt"
        mime_type = "application/vnd.oasis.opendocument.text"
        file_path = os.path.join(self.result_dir_path, filename)
        with ODTTemplate(self.template_file_path) as tpl:
            get_odt_renderer(self.media_dir_path).render(tpl, context)
            tpl.pack(file_path)
        return ReportGeneratorResult(filename, mime_type, file_path)
