# DiscoverVersion

This package automatically discover version information for a package. It
first asks `git`, and if that fails tries to get the version from package
metadata throught `importlib`. It is intended as a lightweight replacement for
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

__version__ = get_version(__name__)
```

## Tests

Before being able to run tests, you need to execute
```python
pip install -e .[test] 
```
to editably install the code.