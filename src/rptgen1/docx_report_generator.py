# code/src/rptgen1/docx_report_generator.py

from docxtpl import DocxTemplate
from typing import BinaryIO
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult, render_file_basename
from .base_report_generator import BaseReportGenerator


class DOCXReportGenerator(BaseReportGenerator):
    def __init__(
        self,
        file_basename: str,
        convert_to_pdf: bool = False,
        pdf_filter_options: dict = {},
        uno_client_config: UnoClientConfig = UnoClientConfig(),
    ):
        super().__init__(file_basename, convert_to_pdf, pdf_filter_options, uno_client_config)

    def render(
        self, context: dict = {}, image_mapping: dict = {}
    ) -> ReportGeneratorResult:
        try:
            rendered_file_basename = render_file_basename(self.file_basename, context)
            docx_result_file_path = self._join_path(
                self.result_dir_path, rendered_file_basename + ".docx"
            )
            tpl = DocxTemplate(self.template_file_path)
            for embedded_file, dst_file in image_mapping.items():
                dst_file_path = self._join_path(self.media_dir_path, dst_file)
                tpl.replace_pic(embedded_file, dst_file_path)
            tpl.render(context=context)
            tpl.save(docx_result_file_path)

            if self.convert_to_pdf:
                pdf_result_file_path = self._convert_to_pdf(
                    docx_result_file_path, rendered_file_basename
                )
                return ReportGeneratorResult(
                    pdf_result_file_path,
                    "application/pdf",
                    rendered_file_basename + ".pdf",
                )
            else:
                return ReportGeneratorResult(
                    docx_result_file_path,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    rendered_file_basename + ".docx",
                )

        except Exception as e:
            self.cleanup_working_directories()
            raise e
