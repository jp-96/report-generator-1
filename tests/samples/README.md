# Run tests

> This document was created with the assistance of Microsoft Copilot.

## python-docx-template (docxtpl)

The `python-docx-template` library is a powerful tool for working with Microsoft Word documents (DOCX) in Python. It allows users to create and modify DOCX files by using templates. This makes it easy to generate documents with dynamic content, such as reports, invoices, letters, and more, by populating predefined templates with data.

Here are some key features of `python-docx-template`:
- **Template-Based:** You can create a DOCX template with placeholders and populate it with data at runtime.
- **Easy to Use:** It provides a simple API for adding text, tables, images, and other elements to your documents.
- **Customizable:** You can customize the appearance and layout of your documents using Word styles and formatting options.
- **Flexible:** Supports various data types, including text, numbers, dates, and images.
- **Integration:** Can be easily integrated into Python applications and scripts for automated document generation.

**Run the tests:**

```bash
cd code/tests/samples/docx/tests
python -m runtests
```

## python-odt-template (python_odt_template)

The `python-odt-template` library is a useful tool for working with OpenDocument Text (ODT) files in Python. It allows users to create and manipulate ODT files using templates, making it easy to generate documents with dynamic content, such as reports, invoices, letters, and more, by populating predefined templates with data.

Here are some key features of `python-odt-template`:
- **Template-Based:** You can create an ODT template with placeholders and populate it with data at runtime.
- **Easy to Use:** It provides a straightforward API for adding text, tables, images, and other elements to your documents.
- **Customizable:** You can customize the appearance and layout of your documents using styles and formatting options available in ODT.
- **Flexible:** Supports various data types, including text, numbers, dates, and images.
- **Integration:** Can be easily integrated into Python applications and scripts for automated document generation.

**Run the tests:**

```bash
cd code/tests/samples/odt
python -m test
```

## relatorio

The `relatorio` library is a powerful tool for generating various types of reports in different formats such as ODT, PDF, RTF, and more, in Python. It is designed to be highly flexible and versatile, allowing users to create complex and detailed reports by merging templates with data. This library is often used in applications where dynamic report generation is required, such as business intelligence, data analysis, and documentation.

Here are some key features of `relatorio`:
- **Template-Based:** You can create templates in various formats and populate them with data at runtime.
- **Versatile Output:** Supports multiple output formats, including ODT, PDF, RTF, HTML, and more.
- **Data Integration:** Can easily integrate with various data sources and formats, including XML, JSON, and Python objects.
- **Customizable:** Provides extensive customization options for styling and formatting reports.
- **Extensible:** Allows for the creation of custom templates and extensions to meet specific reporting needs.

**Run the tests:**

```bash
cd code/tests/samples/relatorio/tests
python -m unittest
```

**Run the examples:**

```bash
cd code/tests/samples/relatorio/examples
python -m demo_chart
python -m demo_context
python -m demo_odf
python -m demo_repository
```

## License Information

- **python-docx-template** (docxtpl) is licensed under the [GNU Lesser General Public License v2.1 (LGPL-2.1)](https://opensource.org/licenses/LGPL-2.1).
- **python-odt-template** (python_odt_template) is licensed under the [MIT License](https://opensource.org/licenses/MIT).
- **relatorio** is licensed under the [GNU Lesser General Public License v3 (LGPL-3.0)](https://www.gnu.org/licenses/lgpl-3.0.html).
