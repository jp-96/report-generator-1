# code/src/rptgen1/odt_report_generator.py

import os
import re
import shutil
import tempfile
from typing import BinaryIO
from jinja2 import Template
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult

prohibited_chars_pattern = r'[<>:"/\\|?*\r\n\t]'


def render_file_basename(file_basename: str, context: dict) -> str:
    rendered_file_basename = Template(file_basename).render(context)
    return re.sub(prohibited_chars_pattern, "_", rendered_file_basename)


class ODTReportGenerator:
    def __init__(
        self,
        file_basename: str,
        convert_to_pdf: bool,
        pdf_filter_options: dict,
        uno_client_config: UnoClientConfig = UnoClientConfig(),
    ):
        self.file_basename = file_basename
        self.convert_to_pdf = convert_to_pdf
        self.pdf_filter_options = pdf_filter_options
        self.uno_client_config = uno_client_config
        # work dir
        self.work_dir_path = tempfile.mkdtemp()
        self.template_dir_path = os.path.join(self.work_dir_path, "template")
        self.media_dir_path = os.path.join(self.work_dir_path, "media")
        self.result_dir_path = os.path.join(self.work_dir_path, "result")

    def cleanup_working_directories(self):
        shutil.rmtree(self.work_dir_path)

    def _save_file(self, file: BinaryIO, filename: str, dir_path: str) -> str:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file_path

    def save_template_file(self, file: BinaryIO, filename: str):
        try:
            os.makedirs(self.template_dir_path, exist_ok=True)
            self.template_file_path = self._save_file(
                file, filename, self.template_dir_path
            )
        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def save_media_file(self, file: BinaryIO, filename: str):
        try:
            os.makedirs(self.media_dir_path, exist_ok=True)
            self._save_file(file, filename, self.media_dir_path)
        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def render(self, context: dict) -> ReportGeneratorResult:
        try:
            rendered_file_basename = render_file_basename(self.file_basename, context)
            os.makedirs(self.result_dir_path, exist_ok=True)
            odt_result_file_path = os.path.join(
                self.result_dir_path, rendered_file_basename + ".odt"
            )
            with ODTTemplate(self.template_file_path) as template:
                get_odt_renderer(self.media_dir_path).render(
                    template,
                    context=context,
                )
                template.pack(odt_result_file_path)
            if not self.convert_to_pdf:
                return ReportGeneratorResult(
                    odt_result_file_path,
                    "application/octet-stream",
                    rendered_file_basename + ".odt",
                )

            pdf_result_file_path = os.path.join(
                self.result_dir_path, rendered_file_basename + ".pdf"
            )
            filter_options = [f"{k}={v}" for k, v in self.pdf_filter_options.items()]
            filtername = "writer_pdf_Export" if filter_options else None
            convert_command = {
                "inpath": odt_result_file_path,
                "outpath": pdf_result_file_path,
                "convert_to": "pdf",
                "filtername": filtername,
                "filter_options": filter_options,
            }
            client.UnoClient(
                self.uno_client_config.server,
                self.uno_client_config.port,
                self.uno_client_config.host_location,
            ).convert(**convert_command)

            return ReportGeneratorResult(
                pdf_result_file_path, "application/pdf", rendered_file_basename + ".pdf"
            )

        except Exception as e:
            self.cleanup_working_directories()
            raise e
