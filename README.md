# report-generator-1

## Install

To install the package from the remote GitHub repository, use the following command:

```bash
sudo pip3 install --upgrade git+https://github.com/jp-96/report-generator-1.git --root-user-action=ignore
```

This command will:
1. Use pip3 to install or upgrade the package.
1. Retrieve the package from the specified GitHub repository URL.
1. Ignore any actions that require root user permissions.

## Install (local)

To install the package locally, follow these steps:

```bash

sudo pip3 install --upgrade build pip
sudo pip3 uninstall -y rptgen1

cd code
python -m build
sudo pip3 install --upgrade . --root-user-action=ignore

```

These commands should be run in the code directory, which in the Docker environment is located at /opt/report-engine/code.

This sequence of commands will:
1. Use pip3 to upgrade the build and pip packages.
1. Uninstall any existing rptgen1 package.
1. Change the directory to code.
1. Build the package using Python's build module.
1. Install the newly built package locally while ignoring any root user actions.

## Unit test - pytest

To run the unit tests using pytest, navigate to the tests directory and execute pytest:

```bash
cd code/tests
pytest
```

The generated files from the tests will be saved in the `tests/result` directory.

## Example - FastAPI Report Engine

To run the FastAPI example for the Report Engine, follow these steps:

```bash
cd code/example/fastapi-report-engine
python main.py
```
Once the server is running, you can access the documentation for the API using one of the following URLs:

1. http://localhost/docs
1. http://localhost:8002/docs

These URLs provide an interactive interface where you can test the endpoints and see the available functionalities of the FastAPI Report Engine.
