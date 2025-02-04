import datetime
from io import BytesIO
import os
import shutil
import pytest
from rptgen1.docx_report_generator import DOCXReportGenerator
from rptgen1.report_generator import create_report_generator
from rptgen1.report_generator_result import ReportGeneratorResult
from rptgen1.uno_client_config import UnoClientConfig


def file_data(templates_directory, file_name):
    file_path = os.path.join(templates_directory, file_name)
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def currnet_datetime():
    td = datetime.timedelta(hours=9)
    tz = datetime.timezone(td, "JST")
    dt = datetime.datetime.now(tz)
    return dt


@pytest.fixture
def current_directory():
    current_dir = os.path.dirname(__file__)
    return current_dir


@pytest.fixture
def results_directory(current_directory):
    result_dir = os.path.join(current_directory, "../results")
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture
def templates_directory(current_directory):
    return os.path.join(current_directory, "samples/docx/tests/templates")


@pytest.fixture
def comments_tpl_docx_file_data(templates_directory):
    return file_data(templates_directory, "comments_tpl.docx")


@pytest.fixture
def order_tpl_docx_file_data(templates_directory):
    return file_data(templates_directory, "order_tpl.docx")


@pytest.fixture
def replace_picture_tpl_docx_file_data(templates_directory):
    return file_data(templates_directory, "replace_picture_tpl.docx")


@pytest.fixture
def python_png_file_data(templates_directory):
    return file_data(templates_directory, "python.png")


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


@pytest.mark.parametrize(
    "convert_to_pdf, file_basename, template_file_name, template_file_data, media_file_name, media_file_data, context, result_basename",
    [
        (
            False,
            "docx_comments",
            "template.docx",
            "comments_tpl_docx_file_data",
            None,
            None,
            None,
            None,
        ),
        (
            True,
            "docx_comments",
            "template.docx",
            "comments_tpl_docx_file_data",
            None,
            None,
            None,
            None,
        ),
        (
            False,
            "docx_order_{{customer_name}}",
            "template.docx",
            "order_tpl_docx_file_data",
            None,
            None,
            "order_tpl_docx_context",
            "docx_order_Eric",
        ),
        (
            True,
            "docx_order_{{customer_name}}",
            "template.docx",
            "order_tpl_docx_file_data",
            None,
            None,
            "order_tpl_docx_context",
            "docx_order_Eric",
        ),
        (
            False,
            "docx_replace_picture",
            "template.docx",
            "replace_picture_tpl_docx_file_data",
            "python_logo.png",
            "python_png_file_data",
            None,
            None,
        ),
        (
            True,
            "docx_replace_picture",
            "template.docx",
            "replace_picture_tpl_docx_file_data",
            "python_logo.png",
            "python_png_file_data",
            None,
            None,
        ),
    ],
)
def test_templates(
    convert_to_pdf,
    file_basename,
    template_file_name,
    template_file_data,
    media_file_name,
    media_file_data,
    context,
    result_basename,
    results_directory,
    request,
):
    template_file_data = request.getfixturevalue(template_file_data)
    if context:
        context = request.getfixturevalue(context)
    if not result_basename:
        result_basename = file_basename
    generator = create_report_generator(
        type="docx",
        file_basename=file_basename,
        convert_to_pdf=convert_to_pdf,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    assert isinstance(generator, DOCXReportGenerator)
    generator.save_template_file(template_file_data, template_file_name)
    if media_file_name:
        media_file_data = request.getfixturevalue(media_file_data)
        generator.save_media_file(media_file_data, media_file_name)

    if context:
        result = generator.render(context)
    else:
        result = generator.render()

    assert isinstance(result, ReportGeneratorResult)
    if convert_to_pdf:
        assert result.mime_type == "application/pdf"
        assert result.filename == result_basename + ".pdf"
    else:
        assert (
            result.mime_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert result.filename == result_basename + ".docx"

    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, os.path.join(results_directory, result.filename))
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)
