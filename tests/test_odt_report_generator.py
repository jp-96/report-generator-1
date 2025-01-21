import pytest
import os
import tempfile
from unittest.mock import MagicMock
from rptgen1.odt_report_generator import ODTReportGenerator, render_file_basename
from rptgen1.uno_client_config import UnoClientConfig
from rptgen1.report_generator_result import ReportGeneratorResult


@pytest.fixture
def context1():
    return {
        "context": {
            "document": {
                "datetime": "2025/01/23 12:34",
                "md_sample": "マークアップテキストです。",
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
                    "capital": "奈良県\u845B\uDB40\uDD02城市",
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
        },
        "file_basename": "renderd_{{document.datetime}}",
        "convert_to_pdf": True,
        "pdf_filter_options": {"Watermark": "draft（下書き）", "SelectPdfVersion": "3"},
    }


@pytest.fixture
def context2():

    return {
        "context": {"image": "writer.png", "city": "奈良県城市"},
        "file_basename": "rendered_{{city}}",
        "convert_to_pdf": True,
        "pdf_filter_options": {},
    }


def test_render_file_basename(context1):
    file_basename = "renderd_{{document.datetime}}"
    rendered_basename = render_file_basename(file_basename, context1["context"])
    assert rendered_basename == "renderd_2025_01_23 12_34"


def test_save_template_file():
    generator = ODTReportGenerator(
        file_basename="test_report", convert_to_pdf=False, pdf_filter_options={}
    )
    template_file_path = "./test_data/simple_template.ja.odt"
    with open(template_file_path, "rb") as f:
        generator.save_template_file(f, "template.odt")
    assert os.path.exists(generator.template_file_path)


def test_save_media_file():
    generator = ODTReportGenerator(
        file_basename="test_report", convert_to_pdf=False, pdf_filter_options={}
    )
    media_file_path = "./test_data/writer.png"
    with open(media_file_path, "rb") as f:
        generator.save_media_file(f, "writer.png")
    assert os.path.exists(os.path.join(generator.media_dir_path, "writer.png"))


# def test_render_context1(context1):
#     generator = ODTReportGenerator(
#         file_basename=context1["file_basename"],
#         convert_to_pdf=context1["convert_to_pdf"],
#         pdf_filter_options=context1["pdf_filter_options"],
#     )
#     generator.template_file_path = "./test_data/simple_template.ja.odt"
#     generator.save_template_file = MagicMock()
#     generator.save_media_file = MagicMock()
#     generator.cleanup_working_directories = MagicMock()
#     generator.uno_client_config = UnoClientConfig()
#     generator.uno_client_config.server = "localhost"
#     generator.uno_client_config.port = 2002
#     generator.uno_client_config.host_location = None

#     result = generator.render(context1["context"])
#     assert isinstance(result, ReportGeneratorResult)
#     assert (
#         result.content_type == "application/pdf"
#         if context1["convert_to_pdf"]
#         else "application/octet-stream"
#     )
#     assert result.filename.endswith(".pdf" if context1["convert_to_pdf"] else ".odt")


def test_render_context2(context2):
    uno_client_config = UnoClientConfig(server="unoserver")
    generator = ODTReportGenerator(
        file_basename=context2["file_basename"],
        convert_to_pdf=context2["convert_to_pdf"],
        pdf_filter_options=context2["pdf_filter_options"],
        uno_client_config=uno_client_config,
    )
    test_data_file_path = "./test_data/template.odt"
    with open(test_data_file_path, "rb") as f:
        generator.save_template_file(f, "template.odt")
    assert os.path.exists(generator.template_file_path)
    test_data_file_path = "./test_data/writer.png"
    with open(test_data_file_path, "rb") as f:
        generator.save_media_file(f, "writer.png")
    assert os.path.exists(os.path.join(generator.media_dir_path, "writer.png"))

    result = generator.render(context2["context"])
    assert isinstance(result, ReportGeneratorResult)
    assert (
        result.mime_type == "application/pdf"
        if context2["convert_to_pdf"]
        else "application/octet-stream"
    )
    assert result.file_name.endswith(".pdf" if context2["convert_to_pdf"] else ".odt")
