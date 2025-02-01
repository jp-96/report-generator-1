# code/src/rptgen1/base_report_generator.py

from abc import ABC, abstractmethod
import os
import re
import shutil
import tempfile
from typing import BinaryIO
from jinja2 import Template
from unoserver import client
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*\r\n\t]', "_", filename)


def render_file_basename(file_basename: str, context: dict) -> str:
    filename = Template(file_basename).render(context)
    return sanitize_filename(filename)


class BaseReportGenerator(ABC):
    def __init__(
        self,
        file_basename: str,
        convert_to_pdf: bool,
        pdf_filter_options: dict,
        uno_client_config: UnoClientConfig,
    ):
        self.file_basename = file_basename
        self.rendered_file_basename = None
        self.convert_to_pdf = convert_to_pdf
        self.pdf_filter_options = pdf_filter_options
        self.uno_client_config = uno_client_config
        self.work_dir_path = tempfile.mkdtemp()
        self.result_dir_path = self._add_work_dir("result")
        self.template_dir_path = self._add_work_dir("template")
        self.media_dir_path = self._add_work_dir("media")
        self.image_mapping = {}  # DocxTemplate.replace_pic()

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
            file_path = self._save_file(file, filename, self.media_dir_path)
            self.image_mapping[filename] = file_path
        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def cleanup_working_directories(self):
        try:
            shutil.rmtree(self.work_dir_path)
        except Exception as e:
            pass

    def _add_work_dir(self, name: str) -> str:
        dir_path = os.path.join(self.work_dir_path, name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def _save_file(self, file: BinaryIO, filename: str, dir_path: str) -> str:
        file_path = os.path.join(dir_path, sanitize_filename(filename))
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file_path

    def _convert_to_pdf(self, inpath: str) -> str:
        filename = self.rendered_file_basename + ".pdf"
        mime_type = "application/pdf"
        file_path = os.path.join(self.result_dir_path, filename)
        filter_options = [f"{k}={v}" for k, v in self.pdf_filter_options.items()]
        convert_command = {
            "inpath": inpath,
            "outpath": file_path,
            "convert_to": "pdf",
            "filtername": "writer_pdf_Export",
            "filter_options": filter_options,
        }
        client.UnoClient(
            self.uno_client_config.server,
            self.uno_client_config.port,
            self.uno_client_config.host_location,
        ).convert(**convert_command)
        return ReportGeneratorResult(file_path, mime_type, filename)

    def render(self, context: dict = {}) -> ReportGeneratorResult:
        try:
            self.rendered_file_basename = render_file_basename(
                self.file_basename, context
            )
            generated = self._render(context)
            if self.convert_to_pdf:
                return self._convert_to_pdf(generated.file_path)
            else:
                return generated

        except Exception as e:
            self.cleanup_working_directories()
            raise e

    @abstractmethod
    def _render(self, context: dict) -> ReportGeneratorResult:
        pass
