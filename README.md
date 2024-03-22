# DiscoverVersion

This package automatically discover version information for a package. It
tries the following option to get the version of the package:

* Inspect a `PKG-INFO` file
* Ask `git`, if the current directory is a git-repository
* Ask `importlib.metadata`
 
It is intended as a lightweight replacement for
`setuptools_scm`.

## Usage

To use automatic version discovery with your build system of choice
, here [`flit`](https://flit.pypa.io/), add the following lines to your
`pyproject.toml`:

```toml
[build-system]
requires = ["flit_core>=3.2", "DiscoverVersion"]
build-backend = "flit_core.buildapi"

[project]
dynamic = ['version']
dependencies = ['DiscoverVersion']
```

The add the following to your toplevel `__init__.py`:

```python3
from DiscoverVersion import get_version

__version__ = get_version('my_package_name')
```

Note that it is important to hard code the name of your package in the call
to `get_version`.

## Tests

Before being able to run tests, you need to execute
```python
pip install -e .[test] 
```
to editably install the code.