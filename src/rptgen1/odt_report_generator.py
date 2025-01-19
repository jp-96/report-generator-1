# rptgen1/odt_report_generator.py

import os
import shutil
import tempfile
from typing import BinaryIO
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from unoserver import client
from .uno_client_config import UnoClientConfig

class ODTReportGenerator:
    """
    A class to generate ODT reports and optionally convert them to PDF.

    Attributes:
        document_content (dict): The content of the document to be rendered.
        file_basename (str): The basename of the file (excluding the extension) to be used for the generated document.
        convert_to_pdf (bool): Indicates if the document should be converted to a PDF file.
        pdf_filter_options (dict): Options for the PDF export filter to be applied during conversion.
        work_dir_path (str): The working directory path for storing temporary files.
        template_dir_path (str): The directory path for storing template files.
        media_dir_path (str): The directory path for storing media files.
        result_dir_path (str): The directory path for storing result files.
    """

    def __init__(self, document_content: dict, file_basename: str, convert_to_pdf: bool, pdf_filter_options: dict, uno_client_config: UnoClientConfig = UnoClientConfig()):
        """
        Initializes the ODTReportGenerator with the given parameters.

        Args:
            document_content (dict): The content of the document to be rendered.
            file_basename (str): The basename of the file (excluding the extension) to be used for the generated document.
            convert_to_pdf (bool): Indicates if the document should be converted to a PDF file.
            pdf_filter_options (dict): Options for the PDF export filter to be applied during conversion.
        """
        self.document_content = document_content
        self.file_basename = file_basename
        self.convert_to_pdf = convert_to_pdf
        self.pdf_filter_options = pdf_filter_options
        self.work_dir_path = tempfile.mkdtemp()
        self.template_dir_path = os.path.join(self.work_dir_path, "template")
        self.media_dir_path = os.path.join(self.work_dir_path, "media")
        self.result_dir_path = os.path.join(self.work_dir_path, "result")
        self.uno_client_config = uno_client_config

    def _initialize_directories(self):
        """Creates the necessary directories for templates, media, and results."""
        try:
            os.makedirs(self.template_dir_path, exist_ok=True)
            os.makedirs(self.media_dir_path, exist_ok=True)
            os.makedirs(self.result_dir_path, exist_ok=True)
        except Exception as e:
            self.cleanup_working_directories()
            raise e
    
    def cleanup_working_directories(self):
        """Cleans up the working directories by removing them."""
        shutil.rmtree(self.work_dir_path)

    def save_file(self, file: BinaryIO, filename: str, dir_path: str) -> str:
        """
        Saves a file to the specified directory.

        Args:
            file (BinaryIO): The file to be saved.
            filename (str): The name of the file.
            dir_path (str): The directory path where the file will be saved.

        Returns:
            str: The path of the saved file.
        """
        self._initialize_directories()
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        return file_path

    def save_template_file(self, file: BinaryIO, filename: str) -> str:
        """
        Saves the template file to the template directory.

        Args:
            file (BinaryIO): The template file to be saved.
            filename (str): The name of the template file.

        Returns:
            str: The path of the saved template file.
        """
        return self.save_file(file, filename, self.template_dir_path)

    def save_media_file(self, file: BinaryIO, filename: str):
        """
        Saves a media file to the media directory.

        Args:
            file (BinaryIO): The media file to be saved.
            filename (str): The name of the media file.
        """
        self.save_file(file, filename, self.media_dir_path)

    def handle_request(self, template_filename: str):
        """
        Handles the report generation request.

        Args:
            template_filename (str): The name of the template file.

        Returns:
            tuple: A tuple containing the file type ("odt" or "pdf") and the path of the result file.
        """
        try:
            template_file_path = os.path.join(self.template_dir_path, template_filename)
            odt_result_file_path = os.path.join(self.result_dir_path, "rendered.odt")
            with ODTTemplate(template_file_path) as template:
                get_odt_renderer(self.media_dir_path).render(
                    template,
                    context=self.document_content,
                )
                template.pack(odt_result_file_path)

            if self.convert_to_pdf:
                return self._convert_to_pdf(odt_result_file_path)

            return "odt", odt_result_file_path

        except Exception as e:
            self.cleanup_working_directories()
            raise e

    def _convert_to_pdf(self, odt_result_file_path: str):
        """
        Converts the generated ODT file to a PDF file.

        Args:
            odt_result_file_path (str): The path of the ODT file to be converted.

        Returns:
            tuple: A tuple containing the file type ("pdf") and the path of the PDF result file.
        """
        pdf_result_file_path = os.path.join(self.result_dir_path, "rendered.pdf")
        filter_options = [f'{k}={v}' for k, v in self.pdf_filter_options.items()]
        filtername = "writer_pdf_Export" if filter_options else None

        convert_command = {
            'inpath': odt_result_file_path,
            'outpath': pdf_result_file_path,
            'convert_to': "pdf",
            'filtername': filtername,
            'filter_options': filter_options
        }
        client.UnoClient(
            self.uno_client_config.server,
            self.uno_client_config.port,
            self.uno_client_config.host_location
        ).convert(**convert_command)

        return "pdf", pdf_result_file_path
