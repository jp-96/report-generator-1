# code/src/rptgen1/base_report_generator.py

from abc import ABC, abstractmethod
import os
import re
import shutil
import tempfile
from typing import BinaryIO
from unoserver import client
from .uno_client_config import UnoClientConfig
from .report_generator_result import ReportGeneratorResult


class BaseReportGenerator(ABC):
    def __init__(
        self,
        convert_to_pdf: bool,
        pdf_filter_options: dict,
        uno_client_config: UnoClientConfig,
    ):
        self.convert_to_pdf = convert_to_pdf
        self.pdf_filter_options = pdf_filter_options
        self.uno_client_config = uno_client_config
        self.work_dir_path = tempfile.mkdtemp()
        self.result_dir_path = self._add_work_dir("result")

    def cleanup_working_directories(self):
        shutil.rmtree(self.work_dir_path)

    def _add_work_dir(self, folder_name: str) -> str:
        sanitized_folder_name = re.sub(r'[<>:"/\\|?*\.]', "_", folder_name)
        dir_path = os.path.join(self.work_dir_path, sanitized_folder_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def _save_file(self, file: BinaryIO, filename: str, dir_path: str) -> str:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file_path

    def _convert_to_pdf(self, inpath: str, file_basename: str) -> str:
        pdf_result_file_path = os.path.join(
            self.result_dir_path, file_basename + ".pdf"
        )
        filter_options = [f"{k}={v}" for k, v in self.pdf_filter_options.items()]
        filtername = "writer_pdf_Export" if filter_options else None
        convert_command = {
            "inpath": inpath,
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
        return pdf_result_file_path

    @abstractmethod
    def render(self, context: dict) -> ReportGeneratorResult:
        pass
