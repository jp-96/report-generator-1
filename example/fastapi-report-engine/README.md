# Example - FastAPI Report Engine

```bash
cd code/example/fastapi-report-engine
python main.py
```

http://localhost/docs or http://localhost:8002/docs

samples: `./code/tests/samples/odt/inputs`

## simple_template.odt

template: `simple_template.odt`
medias: (unckecked: `Send empty value`)

odt_request:

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

# template.odt

- template: `template.odt`
- medias: `writer.png`
- odt_request:

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