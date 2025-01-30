# Run tests

## For python-docx-template

This section provides instructions on how to run tests for [the python-docx-template library](https://github.com/elapouya/python-docx-template), which is used for working with Microsoft Word documents in Python.

**Run the tests:**

```bash
cd code/tests/samples/docx/tests
python -m runtests
```

## For python_odt_template

This section covers the steps needed to run tests for [the python_odt_template library](https://github.com/Tobi-De/python-odt-template), which is used for working with OpenDocument Text (ODT) files in Python. It includes preparation steps for installing necessary software and running the tests.

**Preparation Steps:**

```bash
sudo apt update
sudo apt install libreoffice -y
```

**Run the tests:**

```bash
cd code/tests/samples/odt
python -m test
```
