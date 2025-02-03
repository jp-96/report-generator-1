import datetime
import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from main import app


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
def simple_template_odt_file_path(odt_directory):
    return Path(odt_directory).joinpath("simple_template.odt")


@pytest.fixture
def simple_template_odt_file_reader(simple_template_odt_file_path):
    return open(simple_template_odt_file_path, "rb")


@pytest.fixture
def currnet_datetime():
    td = datetime.timedelta(hours=9)
    tz = datetime.timezone(td, "JST")
    dt = datetime.datetime.now(tz)
    return dt


@pytest.fixture
def readme_md_file_text(odt_directory):
    file_path = os.path.join(odt_directory, "README.md")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def template_odt_file_path(odt_directory):
    return Path(odt_directory).joinpath("template.odt")


@pytest.fixture
def template_odt_file_reader(template_odt_file_path):
    return open(template_odt_file_path, "rb")


@pytest.fixture
def writer_png_file_path(odt_directory):
    return Path(odt_directory).joinpath("writer.png")


@pytest.fixture
def writer_png_file_reader(writer_png_file_path):
    return open(writer_png_file_path, "rb")


@pytest.fixture
def docx_directory(current_directory):
    return os.path.join(current_directory, "samples/docx")


@pytest.fixture
def order_tpl_docx_file_path(docx_directory):
    return Path(docx_directory).joinpath("order_tpl.docx")


@pytest.fixture
def order_tpl_docx_file_reader(order_tpl_docx_file_path):
    return open(order_tpl_docx_file_path, "rb")


@pytest.fixture
def replace_picture_tpl_docx_file_path(docx_directory):
    return Path(docx_directory).joinpath("replace_picture_tpl.docx")


@pytest.fixture
def replace_picture_tpl_docx_file_reader(replace_picture_tpl_docx_file_path):
    return open(replace_picture_tpl_docx_file_path, "rb")


@pytest.fixture
def python_png_file_path(docx_directory):
    return Path(docx_directory).joinpath("python.png")


@pytest.fixture
def python_png_file_reader(python_png_file_path):
    return open(python_png_file_path, "rb")


client = TestClient(app)


def test_komainu_post_simple_template_odt(
    results_directory,
    simple_template_odt_file_reader,
):

    request_data = {
        "context": {
            "document": {
                "datetime": "currnet_datetime",
                "md_sample": "readme_md_file_text",
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
        "file_basename": "rendered",
        "convert_to_pdf": False,
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

    with open(
        os.path.join(results_directory, "komainu_simple_template.odt"), "wb"
    ) as f:
        f.write(response.content)


def test_komainu_post_simple_template_odt_pdf(
    results_directory,
    simple_template_odt_file_reader,
):

    request_data = {
        "context": {
            "document": {
                "datetime": "currnet_datetime",
                "md_sample": "readme_md_file_text",
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
        "file_basename": "rendered",
        "convert_to_pdf": True,
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
    assert b"%PDF" in response.content

    with open(
        os.path.join(results_directory, "komainu_simple_template_odt.pdf"), "wb"
    ) as f:
        f.write(response.content)


def test_komainu_post_template_odt(
    results_directory,
    template_odt_file_reader,
    writer_png_file_reader,
    simple_template_odt_file_reader,
):

    request_data = {
        "context": {"image": "writer.png"},
        "file_basename": "rendered",
        "convert_to_pdf": False,
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

    with open(os.path.join(results_directory, "komainu_template.odt"), "wb") as f:
        f.write(response.content)


def test_komainu_post_template_odt_pdf(
    results_directory, template_odt_file_reader, writer_png_file_reader
):

    request_data = {
        "context": {"image": "writer.png"},
        "file_basename": "rendered",
        "convert_to_pdf": True,
        "pdf_filter_options": {},
    }

    files = {
        "request": (None, json.dumps(request_data), "application/json"),
        "template": (
            "template.odt",
            template_odt_file_reader,
            "application/vnd.oasis.opendocument.text",
        ),
        "medias": ("writer.png", writer_png_file_reader, "image/png"),
    }

    response = client.post("/komainu", files=files)
    assert response.status_code == 200
    assert b"%PDF" in response.content

    with open(os.path.join(results_directory, "komainu_template_odt.pdf"), "wb") as f:
        f.write(response.content)


def test_komainu_post_order_tpl_docx(results_directory, order_tpl_docx_file_reader):

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
        "file_basename": "rendered_{{customer_name}}",
        "convert_to_pdf": False,
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

    with open(os.path.join(results_directory, "komainu_order_tpl.docx"), "wb") as f:
        f.write(response.content)


def test_komainu_post_order_tpl_docx_pdf(results_directory, order_tpl_docx_file_reader):

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
        "file_basename": "rendered_{{customer_name}}",
        "convert_to_pdf": True,
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
    assert b"%PDF" in response.content

    with open(os.path.join(results_directory, "komainu_order_tpl.pdf"), "wb") as f:
        f.write(response.content)

def test_komainu_post_replace_picture_tpl_docx(
    results_directory, replace_picture_tpl_docx_file_reader, python_png_file_reader
):

    request_data = {
        "context": {"name": "python"},
        "file_basename": "rendered_{{name}}",
        "convert_to_pdf": False,
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

    with open(os.path.join(results_directory, "komainu_replace_picture_tpl.docx"), "wb") as f:
        f.write(response.content)


def test_komainu_post_replace_picture_tpl_docx_pdf(
    results_directory, replace_picture_tpl_docx_file_reader, python_png_file_reader
):

    request_data = {
        "context": {"name": "python"},
        "file_basename": "rendered_{{name}}",
        "convert_to_pdf": True,
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
    assert b"%PDF" in response.content

    with open(os.path.join(results_directory, "komainu_replace_picture_tpl_docx.pdf"), "wb") as f:
        f.write(response.content)
