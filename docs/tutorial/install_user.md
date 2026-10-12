# Installation as a user

It is recommended to use python 3.12 with a dedicated virtual environment for this package. Learn how to manage [python versions](https://github.com/pyenv/pyenv) and [virtual environments](https://realpython.com/python-virtual-environments-a-primer/).

There are many alternatives to managing virtual environments and package dependencies (requirements). We recommend using [`uv`](https://github.com/astral-sh/uv), an extremely fast manager Python package and project manager. In this tutorial, you will find paralleled descriptions for `uv`, Python virtual environments (`venv` and `pip`), and [`conda`](https://www.anaconda.com/docs/tools/working-with-conda/environments).

The library can be used on Unix, Windows, provided a Python version is installed. Mac should also be supported but received any feedback if that is true for Mac.

## Setup

Start by creating a virtual environment, e.g., in a directory on your local computer:

=== "uv"
    `uv` is capable of creating a virtual environment and install the required Python version at the same time.

    ```bash
    uv venv --python 3.12
    ```

=== "venv"
    Note that you will need to install the Python version manually beforehand.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    
=== "conda"
    Note that you will need to install the Python version manually beforehand.
    
    ```bash
    conda create -n venv python=3.12
    conda activate venv
    conda install pip
    ```
That command creates a new virtual environment in a directory called `.venv`.

## Installation

Install the latest stable version of this package from PyPI with


=== "uv"

    ```bash
    uv pip install ifes-apt-tc-data-modeling[ipynb]
    ```

=== "pip"


    ```bash
    pip install ifes-apt-tc-data-modeling[ipynb]
    ```

=== "conda"

    ```bash
    python -m pip install ifes-apt-tc-data-modeling[ipynb]
    ```

This will install the module and [jupyterlab](https://jupyterlab.readthedocs.io/en/latest/) whereby the notebook
with examples become executable. 

## Start using `ifes-apt-tc-data-modeling`

The jupyterlab server is started with

=== "uv"

    ```bash
    uv run jupyter-lab
    ```
    
=== "venv"

    ```bash
    jupyter-lab
    ```
    
=== "conda"

    ```bash
    conda run jupyter-lab
    ```

The notebook to run is the following `examples/ExamplesForUsersOrDevelopers.ipynb`
That's it! You can now use the library that you have installed!



