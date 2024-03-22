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
import subprocess


class CannotDiscoverVersion(Exception):
    pass


def get_version_from_git(package_name):
    """
    Discover version from git repository.
    """
    if not os.path.exists('.git'):
        raise CannotDiscoverVersion('.git subdirectory does not exist.')

    if package_name != 'flit_core' and not os.path.exists(package_name):
        raise CannotDiscoverVersion(f"Wrong git repository: Subdirectory '{package_name}' does not exist.")

    try:
        git_describe = subprocess.run(
            ['git', 'describe', '--tags', '--dirty', '--always'],
            stdout=subprocess.PIPE)
    except FileNotFoundError:
        git_describe = None
    if git_describe is None or git_describe.returncode != 0:
        raise CannotDiscoverVersion('git execution failed.')
    version = git_describe.stdout.decode('latin-1').strip()

    dirty = version.endswith('-dirty')

    # Make version PEP 440 compliant
    if dirty:
        version = version.replace('-dirty', '')
    version = version.strip('v')  # Remove leading 'v' if it exists
    version = version.replace('-', '.dev', 1)
    version = version.replace('-', '+', 1)
    if dirty:
        version += '.dirty'

    return version


def get_version(package_name, use_git=True, use_importlib=True):
    """
    Discover version of package `package_name`.

    Parameters
    ----------
    package_name : str
        Name of the package.
    use_git : bool, optional
        Try to discover version from git. (Default: true)
    use_importlib : bool, optional
        Try to discover version from importlib. (Default: true)

    Returns
    -------
    version : str
        Version string.    
    """
    discovered_version = None
    tried = ''

    # If package_name is a submodule, we need to strip the submodule part
    s = package_name.split('.')
    package_name = s[0]

    # We need to start with importlib because otherwise all packages will
    # have the version of the current git repository

    # git works if we are in the source repository
    if discovered_version is None and use_git:
        try:
            discovered_version = get_version_from_git(package_name)
        except CannotDiscoverVersion:
            tried += ', git'
            discovered_version = None

    # importlib is present in Python >= 3.8
    if discovered_version is None and use_importlib:
        try:
            from importlib.metadata import version

            discovered_version = version(package_name)
        except ImportError:
            tried += ', importlib'
            discovered_version = None

    # Nope. Out of options.

    if discovered_version is None:
        raise CannotDiscoverVersion(f'Tried: {tried[2:]}')

    return discovered_version

