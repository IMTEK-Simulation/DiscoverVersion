# DiscoverVersion

This package automatically discover version information for a package. It
first asks `importlib`, and if that fails tries to get the version from local
`git` repository. It is intended as a lightweight replacement for
`setuptools_scm`.

## Tests

Before being able to run tests, you need to execute
```python
pip install -e .[test] 
```
to editably install the code.