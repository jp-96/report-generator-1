# code/tests/test_samples_odt.py

import datetime
from io import BytesIO
from pathlib import Path
import shutil
import pytest
import os
from rptgen1.odt_report_generator import ODTReportGenerator
from rptgen1.report_generator import create_report_generator
from rptgen1.report_generator_result import ReportGeneratorResult
from rptgen1.uno_client_config import UnoClientConfig


def read_as_bytesio(file_path):
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


def file_data(templates_directory, file_name):
    file_path = os.path.join(templates_directory, file_name)
    return read_as_bytesio(file_path)


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
    return os.path.join(current_directory, "samples/odt/inputs")


@pytest.fixture
def simple_template_odt_file_data(templates_directory):
    return file_data(templates_directory, "simple_template.odt")


@pytest.fixture
def readme_md_file_text(templates_directory):
    file_path = os.path.join(templates_directory, "README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def simple_template_odt_context(readme_md_file_text):
    return {
        "document": {
            "datetime": "2025/01/23 04:56",
            "md_sample": readme_md_file_text,
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"],
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {
                "country": "Japan",
                "capital": "Tokio",
                "cities": ["hiroshima", "nagazaki"],
            },
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"],
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {
                "country": "Mexico",
                "capital": "MExico City",
                "cities": ["puebla", "cancun"],
            },
        ],
    }


@pytest.fixture
def template_odt_file_path(templates_directory):
    return Path(templates_directory).joinpath("template.odt")


@pytest.fixture
def template_odt_file_data(template_odt_file_path):
    return read_as_bytesio(template_odt_file_path)


@pytest.fixture
def writer_png_file_path(templates_directory):
    return Path(templates_directory).joinpath("writer.png")


@pytest.fixture
def writer_png_file_data(writer_png_file_path):
    return read_as_bytesio(writer_png_file_path)


@pytest.fixture
def template_odt_context():
    return {"image": "writer.png"}


@pytest.mark.parametrize(
    "convert_to_pdf, file_basename, template_file_name, template_file_data, media_file_name, media_file_data, context, result_basename",
    [
        (
            False,
            "odt_simple_template_{{document.datetime}}",
            "template.odt",
            "simple_template_odt_file_data",
            None,
            None,
            "simple_template_odt_context",
            "odt_simple_template_2025_01_23 04_56",
        ),
        (
            True,
            "odt_simple_template_{{document.datetime}}",
            "template.odt",
            "simple_template_odt_file_data",
            None,
            None,
            "simple_template_odt_context",
            "odt_simple_template_2025_01_23 04_56",
        ),
        (
            False,
            "odt_template",
            "template.odt",
            "template_odt_file_data",
            "writer.png",
            "writer_png_file_data",
            "template_odt_context",
            None,
        ),
        (
            True,
            "odt_template",
            "template.odt",
            "template_odt_file_data",
            "writer.png",
            "writer_png_file_data",
            "template_odt_context",
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
        type="odt",
        file_basename=file_basename,
        convert_to_pdf=convert_to_pdf,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    assert isinstance(generator, ODTReportGenerator)
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
        assert result.mime_type == "application/vnd.oasis.opendocument.text"
        assert result.filename == result_basename + ".odt"

    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, os.path.join(results_directory, result.filename))
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_template_proc(
    results_directory,
    template_odt_context,
    template_odt_file_path,
    writer_png_file_path,
):
    generator = create_report_generator(
        type="odt",
        file_basename="proc_odt2pdf",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server=""),
    )
    assert isinstance(generator, ODTReportGenerator)
    generator.save_template_file(template_odt_file_path, "template.odt")
    generator.save_media_file(writer_png_file_path, "writer.png")
    result = generator.render(template_odt_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.filename == "proc_odt2pdf.pdf"
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, os.path.join(results_directory, result.filename))
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)
