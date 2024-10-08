#
# Copyright 2024 Lars Pastewka
#
# ### MIT license
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import shutil
import subprocess
from pathlib import Path

_toplevel_package = __name__.split(".")[0]
_build_systems = ["flit_core"]


class CannotDiscoverVersion(Exception):
    pass


def get_version_from_git(dirname):
    """
    Discover version from git repository.
    """
    if shutil.which("git") is None:
        raise CannotDiscoverVersion("git executable does not exist.")

    path = Path(os.path.abspath(dirname))
    while path.parent != path and not path.joinpath(".git").exists():
        path = path.parent

    if not path.joinpath(".git").exists():
        raise CannotDiscoverVersion(".git directory does not exist.")

    try:
        git_describe = subprocess.run(
            [
                "git",
                "-c",
                "safe.directory='*'",
                "describe",
                "--tags",
                "--dirty",
                "--always",
            ],
            cwd=str(path),
            stdout=subprocess.PIPE,
        )
    except FileNotFoundError:
        git_describe = None
    if git_describe is None or git_describe.returncode != 0:
        raise CannotDiscoverVersion("git execution failed.")
    version = git_describe.stdout.decode("latin-1").strip()

    dirty = version.endswith("-dirty")

    # Make version PEP 440 compliant
    if dirty:
        version = version.replace("-dirty", "")
    version = version.strip("v")  # Remove leading 'v' if it exists
    version = version.replace("-", ".dev", 1)
    version = version.replace("-", "+", 1)
    if dirty:
        if "+" in version:
            version += ".dirty"
        else:
            version += "+dirty"

    return version


def get_version_from_pkginfo():
    """
    Discover version from PKG-INFO file.
    """
    if not os.path.exists("PKG-INFO"):
        raise CannotDiscoverVersion("PKG-INFO file does not exist.")

    with open("PKG-INFO", "r") as f:
        for line in f:
            if line.startswith("Version: "):
                return line.split()[1]

    raise CannotDiscoverVersion("Version not found in PKG-INFO.")


def get_version(
    package_name, file_name, use_git=True, use_importlib=True, use_pkginfo=True
):
    """
    Discover version of package `package_name`.

    Parameters
    ----------
    package_name : str
        Name of the package.
    file_name : str
        Python file of the caller.
    use_git : bool, optional
        Try to discover version from git. (Default: true)
    use_importlib : bool, optional
        Try to discover version from importlib. (Default: true)
    use_pkginfo : bool, optional
        Try to discover version from PKG-INFO file. (Default: true)

    Returns
    -------
    version : str
        Version string.
    """
    discovered_version = None
    tried = ""

    # We need to start with importlib because otherwise all packages will
    # have the version of the current git repository

    # inspect PKG-INFO file (if it exists)
    if discovered_version is None and use_pkginfo:
        tried += ", PKG-INFO"
        try:
            discovered_version = get_version_from_pkginfo()
        except CannotDiscoverVersion:
            discovered_version = None

    # git works if we are in the source repository
    if discovered_version is None and use_git:
        tried += ", git"
        try:
            if os.path.isdir(file_name):
                dirname = file_name
            else:
                dirname = os.path.dirname(file_name)
            discovered_version = get_version_from_git(dirname)
        except CannotDiscoverVersion:
            discovered_version = None

    # importlib is present in Python >= 3.8
    if (
        discovered_version is None
        and _toplevel_package not in _build_systems
        and use_importlib
    ):
        try:
            tried += ", importlib"
            from importlib.metadata import version

            discovered_version = version(package_name)
        except ImportError:
            discovered_version = None

    # Nope. Out of options.

    if discovered_version is None:
        raise CannotDiscoverVersion(f"Tried: {tried[2:]}")

    return discovered_version
