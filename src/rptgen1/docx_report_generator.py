# code/src/rptgen1/docx_report_generator.py

import os
from docxtpl import DocxTemplate
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult
from .base_report_generator import BaseReportGenerator


class DOCXReportGenerator(BaseReportGenerator):
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

    def _render(self, context: dict = {}) -> ReportGeneratorResult:
        filename = self.rendered_file_basename + ".docx"
        mime_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        file_path = os.path.join(self.result_dir_path, filename)
        tpl = DocxTemplate(self.template_file_path)
        for embedded_file, dst_file in self.image_mapping.items():
            tpl.replace_pic(embedded_file, dst_file)
        tpl.render(context=context)
        tpl.save(file_path)
        return ReportGeneratorResult(file_path, mime_type, filename)
