# code/src/rptgen1/odt_report_generator.py

import os
from typing import BinaryIO
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult, render_file_basename
from .base_report_generator import BaseReportGenerator


class ODTReportGenerator(BaseReportGenerator):
    def __init__(
        self,
        file_basename: str,
        convert_to_pdf: bool = False,
        pdf_filter_options: dict = {},
        uno_client_config: UnoClientConfig = UnoClientConfig(),
    ):
        super().__init__(convert_to_pdf, pdf_filter_options, uno_client_config)
        self.file_basename = file_basename
        self.template_dir_path = self._add_work_dir("template")
        self.media_dir_path = self._add_work_dir("media")

    def save_template_file(self, file: BinaryIO, filename: str):
        try:
            self.template_file_path = self._save_file(
                file, filename, self.template_dir_path
            )
        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def save_media_file(self, file: BinaryIO, filename: str):
        try:
            self._save_file(file, filename, self.media_dir_path)
        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def render(self, context: dict) -> ReportGeneratorResult:
        try:
            rendered_file_basename = render_file_basename(self.file_basename, context)
            odt_result_file_path = os.path.join(
                self.result_dir_path, rendered_file_basename + ".odt"
            )
            with ODTTemplate(self.template_file_path) as template:
                get_odt_renderer(self.media_dir_path).render(
                    template,
                    context=context,
                )
                template.pack(odt_result_file_path)

            if self.convert_to_pdf:
                pdf_result_file_path = self._convert_to_pdf(
                    odt_result_file_path, rendered_file_basename
                )
                return ReportGeneratorResult(
                    pdf_result_file_path,
                    "application/pdf",
                    rendered_file_basename + ".pdf",
                )
            else:
                return ReportGeneratorResult(
                    odt_result_file_path,
                    "application/vnd.oasis.opendocument.text",
                    rendered_file_basename + ".odt",
                )

        except Exception as e:
            self.cleanup_working_directories()
            raise e
