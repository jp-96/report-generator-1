from io import BytesIO
import os
import shutil
import pytest
from rptgen1.docx_report_generator import DOCXReportGenerator
from rptgen1.report_generator_result import ReportGeneratorResult
from rptgen1.uno_client_config import UnoClientConfig


@pytest.fixture
def current_directory():
    current_dir = os.path.dirname(__file__)
    return current_dir


@pytest.fixture
def templates_directory(current_directory):
    return os.path.join(current_directory, "samples/docx/tests/templates")


@pytest.fixture
def results_directory(current_directory):
    result_dir = os.path.join(current_directory, "../results")
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture
def comments_tpl_docx_file_data(templates_directory):
    file_path = os.path.join(templates_directory, "comments_tpl.docx")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def order_tpl_docx_file_data(templates_directory):
    file_path = os.path.join(templates_directory, "order_tpl.docx")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def replace_picture_tpl_docx_file_data(templates_directory):
    file_path = os.path.join(templates_directory, "replace_picture_tpl.docx")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def python_png_file_data(templates_directory):
    file_path = os.path.join(templates_directory, "python.png")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def order_tpl_docx_context():
    context = {
        "customer_name": "Eric",
        "items": [
            {"desc": "Python interpreters", "qty": 2, "price": "FREE"},
            {"desc": "Django projects", "qty": 5403, "price": "FREE"},
            {"desc": "Guido", "qty": 1, "price": "100,000,000.00"},
        ],
        "in_europe": True,
        "is_paid": False,
        "company_name": "The World Wide company",
        "total_price": "100,000,000.00",
    }
    return context


def test_comments_tpl_docx(results_directory, comments_tpl_docx_file_data):
    generator = DOCXReportGenerator(
        file_basename="comments",
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(comments_tpl_docx_file_data, "template.docx")
    result = generator.render()
    assert isinstance(result, ReportGeneratorResult)
    assert (
        result.mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert result.filename.endswith(".docx")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_comments_tpl_docx_pdf(results_directory, comments_tpl_docx_file_data):
    generator = DOCXReportGenerator(
        file_basename="comments",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(comments_tpl_docx_file_data, "template.docx")
    result = generator.render()
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.filename.endswith(".pdf")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_order_tpl_docx(
    results_directory, order_tpl_docx_file_data, order_tpl_docx_context
):
    generator = DOCXReportGenerator(
        file_basename="order",
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(order_tpl_docx_file_data, "template.docx")
    result = generator.render(order_tpl_docx_context)
    assert isinstance(result, ReportGeneratorResult)
    assert (
        result.mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert result.filename.endswith(".docx")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_order_tpl_docx_pdf(
    results_directory, order_tpl_docx_file_data, order_tpl_docx_context
):
    generator = DOCXReportGenerator(
        file_basename="order",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(order_tpl_docx_file_data, "template.docx")
    result = generator.render(order_tpl_docx_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.filename.endswith(".pdf")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_replace_picture_docx(
    results_directory, replace_picture_tpl_docx_file_data, python_png_file_data
):
    generator = DOCXReportGenerator(
        file_basename="replace_picture",
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(replace_picture_tpl_docx_file_data, "template.docx")
    generator.save_media_file(python_png_file_data, "python_logo.png")
    result = generator.render()
    assert isinstance(result, ReportGeneratorResult)
    assert (
        result.mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert result.filename.endswith(".docx")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_replace_picture_docx_pdf(
    results_directory, replace_picture_tpl_docx_file_data, python_png_file_data
):
    generator = DOCXReportGenerator(
        file_basename="replace_picture",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(replace_picture_tpl_docx_file_data, "template.docx")
    generator.save_media_file(python_png_file_data, "python_logo.png")
    result = generator.render()
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.filename.endswith(".pdf")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)
