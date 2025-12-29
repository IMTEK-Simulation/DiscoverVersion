# DiscoverVersion

This package automatically discovers version information for a package. It
tries the following options to get the version of the package (in order):

* Check the `DISCOVER_VERSION` environment variable
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

Then add the following to your toplevel `__init__.py`:

```python3
from DiscoverVersion import get_version

__version__ = get_version('my_package_name')
```

Note that it is important to hard code the name of your package in the call
to `get_version`.

## Environment Variable Override

You can override version discovery by setting the `DISCOVER_VERSION` environment
variable. This is useful in CI/CD pipelines where git may not be available or
when building in isolated environments:

```bash
DISCOVER_VERSION=1.2.3 python -m build
```

## Command Line Interface

DiscoverVersion provides a CLI for discovering and outputting version information:

```bash
# Print the discovered version
python -m DiscoverVersion

# Or use the entry point
discover-version

# Write version to a Python file
python -m DiscoverVersion --write-to version.py

# Write version to a plain text file (useful for Meson builds)
python -m DiscoverVersion --write-to version.txt --plain

# Specify a fallback version if discovery fails
python -m DiscoverVersion --fallback 0.0.0

# Disable specific discovery methods
python -m DiscoverVersion --no-git --no-env
```

### CI/CD Example (GitHub Actions)

Here's an example of using DiscoverVersion in a GitHub Actions workflow with
`cibuildwheel`:

```yaml
- name: Get version from DiscoverVersion
  id: get_version
  run: |
    pip install DiscoverVersion
    echo "version=$(python -m DiscoverVersion)" >> $GITHUB_OUTPUT

- name: Build wheels
  uses: pypa/cibuildwheel@v2
  env:
    CIBW_ENVIRONMENT: DISCOVER_VERSION=${{ steps.get_version.outputs.version }}
```

## Tests

Before being able to run tests, you need to execute
```python
pip install -e .[test] 
```
to editably install the code.