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

"""
Meson-python metadata provider for DiscoverVersion.

This module provides version discovery integration with meson-python build
backend. To use it, add the following to your pyproject.toml:

    [tool.meson-python.metadata]
    version.provider = "DiscoverVersion.meson_python"

"""

from pathlib import Path
from typing import Any, Mapping

from .discovery import (
    CannotDiscoverVersion,
    get_version_from_env,
    get_version_from_git,
    get_version_from_pkginfo,
)


class MesonPythonMetadataProvider:
    """
    Metadata provider for meson-python.

    This class follows the meson-python metadata provider interface.
    """

    def __call__(self, source_dir: Path) -> Mapping[str, Any]:
        """
        Return package metadata including version.

        Parameters
        ----------
        source_dir : Path
            Path to the source directory.

        Returns
        -------
        dict
            Dictionary with 'version' key.
        """
        version = None

        # Check environment variable override first (highest priority)
        version = get_version_from_env()

        # Try PKG-INFO (for sdist builds)
        if version is None:
            try:
                import os
                old_cwd = os.getcwd()
                os.chdir(source_dir)
                try:
                    version = get_version_from_pkginfo()
                finally:
                    os.chdir(old_cwd)
            except CannotDiscoverVersion:
                pass

        # Try git
        if version is None:
            try:
                version = get_version_from_git(source_dir)
            except CannotDiscoverVersion:
                pass

        if version is None:
            raise CannotDiscoverVersion(
                "Could not discover version from environment, PKG-INFO, or git"
            )

        return {"version": version}


# Module-level callable for meson-python
__call__ = MesonPythonMetadataProvider()
