import datetime
import json
import os
from pathlib import Path

import urllib
import urllib.parse
from fastapi.testclient import TestClient
import pytest

from main import app


def extract_filename_from_response(response):
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        if "filename*=utf-8''" in content_disposition:
            filename = content_disposition.split("filename*=utf-8''")[-1]
            filename = urllib.parse.unquote(filename)
            return filename
        elif "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')
            return filename
        else:
            return None
    else:
        return None


@pytest.fixture
def currnet_datetime():
    td = datetime.timedelta(hours=9)
    tz = datetime.timezone(td, "JST")
    dt = datetime.datetime.now(tz)
    return str(dt)


@pytest.fixture
def current_directory():
    current_dir = os.path.dirname(__file__)
    return current_dir


@pytest.fixture
def results_directory(current_directory):
    result_dir = os.path.join(current_directory, "../../../results")
    os.makedirs(result_dir, exist_ok=True)
    return result_dir


@pytest.fixture
def odt_directory(current_directory):
    return os.path.join(current_directory, "samples/odt")


@pytest.fixture
def simple_template_odt_file_reader(odt_directory):
    file_path = Path(odt_directory).joinpath("simple_template.odt")
    return open(file_path, "rb")


@pytest.fixture
def readme_md_file_text(odt_directory):
    file_path = os.path.join(odt_directory, "README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def template_odt_file_reader(odt_directory):
    file_path = Path(odt_directory).joinpath("template.odt")
    return open(file_path, "rb")


@pytest.fixture
def writer_png_file_reader(odt_directory):
    file_path = Path(odt_directory).joinpath("writer.png")
    return open(file_path, "rb")


@pytest.fixture
def docx_directory(current_directory):
    return os.path.join(current_directory, "samples/docx")


@pytest.fixture
def order_tpl_docx_file_path(docx_directory):
    return Path(docx_directory).joinpath("order_tpl.docx")


@pytest.fixture
def order_tpl_docx_file_reader(docx_directory):
    file_path = Path(docx_directory).joinpath("order_tpl.docx")
    return open(file_path, "rb")


@pytest.fixture
def replace_picture_tpl_docx_file_reader(docx_directory):
    file_path = Path(docx_directory).joinpath("replace_picture_tpl.docx")
    return open(file_path, "rb")


@pytest.fixture
def python_png_file_reader(docx_directory):
    file_path = Path(docx_directory).joinpath("python.png")
    return open(file_path, "rb")


client = TestClient(app)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_simple_template_odt(
    convert_to_pdf,
    results_directory,
    simple_template_odt_file_reader,
    currnet_datetime,
    readme_md_file_text,
):

    request_data = {
        "context": {
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
        },
        "file_basename": "komainu_odt_simple_template_{{document.datetime}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "simple_template.odt",
            simple_template_odt_file_reader,
            "application/vnd.oasis.opendocument.text",
        ),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"application/vnd.oasis.opendocument.text" in response.content

    result_filename = extract_filename_from_response(response)
    with open(os.path.join(results_directory, result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_template_odt(
    convert_to_pdf,
    results_directory,
    template_odt_file_reader,
    writer_png_file_reader,
    simple_template_odt_file_reader,
):

    request_data = {
        "context": {"image": "writer.png"},
        "file_basename": "komainu_odt_template",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = [
        ("request", (None, json.dumps(request_data), "application/json")),
        (
            "template",
            (
                "template.odt",
                template_odt_file_reader,
                "application/vnd.oasis.opendocument.text",
            ),
        ),
        ("medias", ("writer.png", writer_png_file_reader, "image/png")),
        (
            "medias",
            (
                "simple_template.odt",
                simple_template_odt_file_reader,
                "application/vnd.oasis.opendocument.text",
            ),
        ),
    ]

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"application/vnd.oasis.opendocument.text" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_odt_template.pdf"
    else:
        assert result_filename == "komainu_odt_template.odt"
    with open(os.path.join(results_directory, result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_order_tpl_docx(
    convert_to_pdf, results_directory, order_tpl_docx_file_reader
):

    request_data = {
        "context": {
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
        },
        "file_basename": "komainu_docx_order_{{customer_name}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = [
        ("request", (None, json.dumps(request_data), "application/json")),
        (
            "template",
            (
                "order_tpl.docx",
                order_tpl_docx_file_reader,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        ),
    ]

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"word/document.xml" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_docx_order_Eric.pdf"
    else:
        assert result_filename == "komainu_docx_order_Eric.docx"
    with open(os.path.join(results_directory, result_filename), "wb") as f:
        f.write(response.content)


@pytest.mark.parametrize("convert_to_pdf", [False, True])
def test_komainu_post_replace_picture_tpl_docx(
    convert_to_pdf,
    results_directory,
    replace_picture_tpl_docx_file_reader,
    python_png_file_reader,
):

    request_data = {
        "context": {"name": "python"},
        "file_basename": "komainu_docx_replace_picture_{{name}}",
        "convert_to_pdf": convert_to_pdf,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "replace_picture_tpl.docx",
            replace_picture_tpl_docx_file_reader,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        # image tag: python_logo.png
        "medias": ("python_logo.png", python_png_file_reader, "image/png"),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200

    if convert_to_pdf:
        assert b"%PDF" in response.content
    else:
        assert b"word/document.xml" in response.content

    result_filename = extract_filename_from_response(response)
    if convert_to_pdf:
        assert result_filename == "komainu_docx_replace_picture_python.pdf"
    else:
        assert result_filename == "komainu_docx_replace_picture_python.docx"
    with open(os.path.join(results_directory, result_filename), "wb") as f:
        f.write(response.content)
