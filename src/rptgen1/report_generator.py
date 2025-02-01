# code/src/rptgen1/report_generator.py


from .odt_report_generator import ODTReportGenerator
from .docx_report_generator import DOCXReportGenerator
from .uno_client_config import UnoClientConfig


def create_odt(
    file_basename: str,
    convert_to_pdf: bool,
    pdf_filter_options: dict,
    uno_client_config: UnoClientConfig,
):
    return ODTReportGenerator(
        file_basename, convert_to_pdf, pdf_filter_options, uno_client_config
    )


def create_docx(
    file_basename: str,
    convert_to_pdf: bool,
    pdf_filter_options: dict,
    uno_client_config: UnoClientConfig,
):
    return DOCXReportGenerator(
        file_basename, convert_to_pdf, pdf_filter_options, uno_client_config
    )


def create_report_generator(
    type: str,
    file_basename: str,
    convert_to_pdf: bool = False,
    pdf_filter_options: dict = {},
    uno_client_config: UnoClientConfig = UnoClientConfig(),
):
    if type == "odt":
        return create_odt(
            file_basename, convert_to_pdf, pdf_filter_options, uno_client_config
        )
    elif type == "docx":
        return create_docx(
            file_basename, convert_to_pdf, pdf_filter_options, uno_client_config
        )
    else:
        raise ValueError("Unsupported type. Please use 'odt' or 'docx'.")
