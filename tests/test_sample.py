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
def sample_file_directory(current_directory):
    return os.path.join(current_directory, "sample")


@pytest.fixture
def result_file_directory(current_directory):
    result_dir = os.path.join(current_directory, "result")
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture
def simple_template_odt_file_data(sample_file_directory):
    file_path = os.path.join(sample_file_directory, "simple_template.odt")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def readme_md_file_text(sample_file_directory):
    file_path = os.path.join(sample_file_directory, "README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def simple_template_odt_context(readme_md_file_text):
    return {
        "document": {
            "datetime": datetime.datetime.now(),
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
def template_odt_file_data(sample_file_directory):
    file_path = os.path.join(sample_file_directory, "template.odt")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def writer_png_file_data(sample_file_directory):
    file_path = os.path.join(sample_file_directory, "writer.png")
    with open(file_path, "rb") as file:
        return BytesIO(file.read())


@pytest.fixture
def template_odt_context():
    return {"image": "writer.png"}

def test_simple_template_odt(
    result_file_directory,
    simple_template_odt_context,
    simple_template_odt_file_data
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
    shutil.copy2(result.file_path, result_file_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)


def test_template_odt(
    result_file_directory,
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
    shutil.copy2(result.file_path, result_file_directory)
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)