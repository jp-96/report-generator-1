# code/tests/test_samples_relatorio.py

import datetime
from io import BytesIO
import os
import shutil
import pytest
from rptgen1.relatorio_report_generator import RelatorioReportGenerator
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
    return os.path.join(current_directory, "samples/relatorio/examples")


@pytest.fixture
def pie_chart_png_file_data(templates_directory):
    return file_data(templates_directory, "pie_chart")


@pytest.fixture
def vbar_chart_svg_file_data(templates_directory):
    return file_data(templates_directory, "vbar_chart")


@pytest.fixture
def basic_tex_file_data(templates_directory):
    return file_data(templates_directory, "basic.tex")


@pytest.fixture
def bouteille_png_file_data(templates_directory):
    return file_data(templates_directory, "bouteille.png")


class Invoice(dict):

    @property
    def total(self):
        return sum(line["amount"] for line in self["lines"])

    @property
    def vat(self):
        return self.total * 0.21


@pytest.fixture
def invoice_context(bouteille_png_file_data):
    inv = Invoice(
        customer={
            "name": "John Bonham",
            "address": {"street": "Smirnov street", "zip": 1000, "city": "Montreux"},
        },
        lines=[
            {
                "item": {"name": "Vodka 70cl", "reference": "VDKA-001", "price": 10.34},
                "quantity": 7,
                "amount": 7 * 10.34,
            },
            {
                "item": {
                    "name": "Cognac 70cl",
                    "reference": "CGNC-067",
                    "price": 13.46,
                },
                "quantity": 12,
                "amount": 12 * 13.46,
            },
            {
                "item": {
                    "name": "Sparkling water 25cl",
                    "reference": "WATR-007",
                    "price": 4,
                },
                "quantity": 1,
                "amount": 4,
            },
            {
                "item": {
                    "name": "Good customer",
                    "reference": "BONM-001",
                    "price": -20,
                },
                "quantity": 1,
                "amount": -20,
            },
        ],
        id="MZY-20080703",
        status="late",
        bottle=(bouteille_png_file_data, "image/png"),
    )
    return inv


@pytest.mark.parametrize(
    "convert_to_pdf, file_basename, template_file_name, template_file_data, media_file_name, media_file_data, context, result_basename",
    [
        (
            False,
            "relatorio_pie_png",
            "pie_chart.png.cha",
            "pie_chart_png_file_data",
            None,
            None,
            "invoice_context",
            None,
        ),
        (
            True,
            "relatorio_pie_png",
            "pie_chart.png.cha",
            "pie_chart_png_file_data",
            None,
            None,
            "invoice_context",
            None,
        ),
        (
            False,
            "relatorio_vbar_svg",
            "vbar_chart.svg.cha",
            "vbar_chart_svg_file_data",
            None,
            None,
            "invoice_context",
            None,
        ),
        (
            True,
            "relatorio_vbar_svg",
            "vbar_chart.svg.cha",
            "vbar_chart_svg_file_data",
            None,
            None,
            "invoice_context",
            None,
        ),
        (
            False,
            "relatorio_basic_tex",
            "basic.tex",
            "basic_tex_file_data",
            None,
            None,
            "invoice_context",
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
        type="relatorio",
        file_basename=file_basename,
        convert_to_pdf=convert_to_pdf,
        pdf_filter_options={},
        uno_client_config=UnoClientConfig(server="unoserver"),
    )
    assert isinstance(generator, RelatorioReportGenerator)
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

    assert os.path.exists(result.file_path)
    shutil.copy2(result.file_path, os.path.join(results_directory, result.filename))
    generator.cleanup_working_directories()
    assert not os.path.exists(result.file_path)
