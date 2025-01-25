# code/tests/test_samples_odt.py

import datetime
from io import BytesIO
import shutil
import pytest
import os
from rptgen1.odt_report_generator import ODTReportGenerator
from rptgen1.report_generator_result import ReportGeneratorResult
from rptgen1.uno_client_config import UnoClientConfig


@pytest.fixture
def current_directory():
    current_dir = os.path.dirname(__file__)
    return current_dir


@pytest.fixture
def inputs_directory(current_directory):
    return os.path.join(current_directory, "samples/odt/inputs")


@pytest.fixture
def results_directory(current_directory):
    result_dir = os.path.join(current_directory, "results")
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture
def simple_template_odt_file_data(inputs_directory):
    file_path = os.path.join(inputs_directory, "simple_template.odt")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def currnet_datetime():
    td = datetime.timedelta(hours=9)
    tz = datetime.timezone(td, "JST")
    dt = datetime.datetime.now(tz)
    return dt


@pytest.fixture
def readme_md_file_text(inputs_directory):
    file_path = os.path.join(inputs_directory, "README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def simple_template_odt_context(currnet_datetime, readme_md_file_text):
    return {
        "document": {
            "datetime": currnet_datetime,
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
def template_odt_file_data(inputs_directory):
    file_path = os.path.join(inputs_directory, "template.odt")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def writer_png_file_data(inputs_directory):
    file_path = os.path.join(inputs_directory, "writer.png")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def template_odt_context():
    return {"image": "writer.png"}


def test_simple_template_odt(
    results_directory, simple_template_odt_context, simple_template_odt_file_data
):
    generator = ODTReportGenerator(
        file_basename="simple_{{document.datetime}}",
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(simple_template_odt_file_data, "template.odt")
    result = generator.render(simple_template_odt_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/vnd.oasis.opendocument.text"
    assert result.file_name.endswith(".odt")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_simple_template_odt_to_pdf(
    results_directory, simple_template_odt_context, simple_template_odt_file_data
):
    generator = ODTReportGenerator(
        file_basename="simple_{{document.datetime}}",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(simple_template_odt_file_data, "template.odt")
    result = generator.render(simple_template_odt_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.file_name.endswith(".pdf")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_template_odt(
    results_directory,
    template_odt_context,
    template_odt_file_data,
    writer_png_file_data,
):
    generator = ODTReportGenerator(
        file_basename="rendered_{{image}}",
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(template_odt_file_data, "template.odt")
    generator.save_media_file(writer_png_file_data, "writer.png")
    result = generator.render(template_odt_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/vnd.oasis.opendocument.text"
    assert result.file_name.endswith(".odt")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_template_odt_to_pdf(
    results_directory,
    template_odt_context,
    template_odt_file_data,
    writer_png_file_data,
):
    generator = ODTReportGenerator(
        file_basename="rendered_{{image}}",
        convert_to_pdf=True,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    generator.save_template_file(template_odt_file_data, "template.odt")
    generator.save_media_file(writer_png_file_data, "writer.png")
    result = generator.render(template_odt_context)
    assert isinstance(result, ReportGeneratorResult)
    assert result.mime_type == "application/pdf"
    assert result.file_name.endswith(".pdf")
    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, results_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)
