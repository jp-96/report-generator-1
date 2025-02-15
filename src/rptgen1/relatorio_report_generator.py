# code/src/rptgen1/relatorio_report_generator.py

import os
from relatorio import Report
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult
from .base_report_generator import BaseReportGenerator

PNG_MIME = "image/png"
SVG_MIME = "image/svg"
PDF_MIME = "application/pdf"
ODT_MIME = "application/vnd.oasis.opendocument.text"
ODS_MIME = "application/vnd.oasis.opendocument.spreadsheet"
ODP_MIME = "application/vnd.oasis.opendocument.presentation"

mime_dict = {
    ".png.cha": (PNG_MIME, ".png"),
    ".svg.cha": (SVG_MIME, ".svg"),
    ".tex": (PDF_MIME, ".pdf"),
    ".odt": (ODT_MIME, ".odt"),
    ".ods": (ODS_MIME, ".ods"),
    ".odp": (ODP_MIME, ".odp"),
}


def get_mime_by_filename(filename):
    filename = str(filename)
    for suffix in mime_dict:
        if filename.endswith(suffix):
            return mime_dict[suffix]
    raise ValueError("Unsupported template file.")


class RelatorioReportGenerator(BaseReportGenerator):
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
        mime_type, file_ext = get_mime_by_filename(self.template_file_path)
        filename = self.rendered_file_basename + file_ext
        file_path = os.path.join(self.result_dir_path, filename)
        report = Report(self.template_file_path, mime_type)
        with open(file_path, "wb") as f:
            f.write(report(o=context).render().getvalue())
        return ReportGeneratorResult(filename, mime_type, file_path)
