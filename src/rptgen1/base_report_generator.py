# code/src/rptgen1/base_report_generator.py

from abc import ABC, abstractmethod
import os
import shutil
import tempfile
from typing import BinaryIO

from .report_generator_result import ReportGeneratorResult

class BaseReportGenerator(ABC):
    def __init__(self):
        self.work_dir_path = tempfile.mkdtemp()
        self.result_dir_path = os.path.join(self.work_dir_path, "result")

    def cleanup_working_directories(self):
        shutil.rmtree(self.work_dir_path)

    def _save_file(self, file: BinaryIO, filename: str, dir_path: str) -> str:
        file_path = os.path.join(dir_path, filename)
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file_path

    @abstractmethod
    def render(self, context: dict) -> ReportGeneratorResult:
        pass
