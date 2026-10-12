# Installation as a developer

Developers should first clone the repository:

```bash
git clone https://www.github.com/atomprobe-tc/ifes-apt-tc-data-modeling.git
cd ifes-apt-tc-data-modeling
```

Next install using e.g., `uv`, a Python virtual environment (venv), 
or a `conda` environment.

=== "uv"

    ```bash
    uv run pip install --upgrade pip
    uv run pip install -e ".[dev,docs,ipynb]"
    ```

=== "venv"

    ```bash
    pip install --upgrade pip
    pip install -e ".[dev,docs,ipynb]"
    ```
    
=== "conda"

    ```bash
    conda run pip install --upgrade pip
    conda run pip install -e ".[dev,docs,ipynb]"
    ```

This will install modules for linting, code styling, and unit testing via the [pytest](https://docs.pytest.org/en/stable) framework.

Unit tests can then be started from the root directory of the installation with respective calls:

=== "uv"

    ```bash
    uv run pytest -sv tests
    ```
    
=== "venv"

    ```bash
    pytest -sv tests
    ```
    
=== "conda"

    ```bash
    conda run pytest -sv tests
    ```
