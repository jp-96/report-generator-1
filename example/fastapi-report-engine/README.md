# Example - FastAPI Report Engine

```bash
cd code/example/fastapi-report-engine
python main.py
```

http://localhost/docs or http://localhost:8002/docs

samples:
- `./code/example/fastapi-report-engine/tests/samples/odt`
- `./code/example/fastapi-report-engine/tests/samples/docx`

## odt - simple_template.odt

- template: `simple_template.odt`
- medias: (unckecked: `Send empty value`)
- request:

```json

{
    "context": {
        "document": {
            "datetime": "2025/01/23 12:34",
            "md_sample": "# This is an H1\n## This is an H2\nMarkdown is a lightweight markup language."
        },
        "countries": [
            {
                "country": "United States",
                "capital": "Washington",
                "cities": ["miami", "new york", "california", "texas", "atlanta"]
            },
            {"country": "England", "capital": "London", "cities": ["gales"]},
            {"country": "Japan", "capital": "Tokio", "cities": ["hiroshima", "nagazaki"]},
            {
                "country": "Nicaragua",
                "capital": "Managua",
                "cities": ["leon", "granada", "masaya"]
            },
            {"country": "Argentina", "capital": "Buenos aires"},
            {"country": "Chile", "capital": "Santiago"},
            {"country": "Mexico", "capital": "MExico City", "cities": ["puebla", "cancun"]}
        ]
    },
    "file_basename": "renderd_{{document.datetime}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {
        "Watermark": "draft",
        "SelectPdfVersion": "3"
    }
}

```

## odt - template.odt

- template: `template.odt`
- medias: `writer.png`
- request:

```json

{
    "context": {
        "image":"writer.png"
    },
    "file_basename": "rendered_{{image}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {}
}

```

## docx - order_tpl.docx

- template: `order_tpl.docx`
- medias: (unckecked: `Send empty value`)
- request:

```json

{
    "context": {
        "customer_name": "Eric",
        "items": [
            {"desc": "Python interpreters", "qty": 2, "price": "FREE"},
            {"desc": "Django projects", "qty": 5403, "price": "FREE"},
            {"desc": "Guido", "qty": 1, "price": "100,000,000.00"}
        ],
        "in_europe": true,
        "is_paid": false,
        "company_name": "The World Wide company",
        "total_price": "100,000,000.00"
    },
    "file_basename": "rendered_{{customer_name}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {}
}

```

## docx - replace_picture_tpl.docx

- template: `replace_picture_tpl.docx`
- medias: `python_logo.png`
- request:

```json

{
    "context": {
        "name":"python"
    },
    "file_basename": "rendered_{{name}}",
    "convert_to_pdf": true,
    "pdf_filter_options": {}
}

```
