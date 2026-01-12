#
# Copyright 2026 Hannes Holey
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
Scikit-build-core metadata provider for DiscoverVersion.

This module provides version discovery integration with scikit-build-core build
backend. To use it, add the following to your pyproject.toml:

    [tool.scikit-build]
    experimental = "true"
    metadata.version.provider = "DiscoverVersion.scikit_build_core"

"""

from .discovery import (
    CannotDiscoverVersion,
    get_version_from_env,
    get_version_from_git,
    get_version_from_pkginfo,
)

__all__ = ["dynamic_metadata", "get_requires_for_dynamic_metadata"]


def __dir__() -> list[str]:
    return __all__


def dynamic_metadata(
    field: str,
    settings: dict[str, object] | None = None,
) -> str:
    # this is a classic implementation, waiting for the release of
    # vcs-versioning and an improved public interface

    if field != "version":
        msg = "Only the 'version' field is supported"
        raise ValueError(msg)

    if settings:
        msg = "No inline configuration is supported"
        raise ValueError(msg)

    version = None

    # Check environment variable override first (highest priority)
    version = get_version_from_env()

    # Try PKG-INFO (for sdist builds)
    if version is None:
        try:
            version = get_version_from_pkginfo()
        except CannotDiscoverVersion:
            pass

    # Try git
    if version is None:
        try:
            import os
            version = get_version_from_git(os.getcwd())
        except CannotDiscoverVersion:
            pass

    if version is None:
        raise CannotDiscoverVersion(
            "Could not discover version from environment, PKG-INFO, or git"
        )

    return version


def get_requires_for_dynamic_metadata(
    _settings: dict[str, object] | None = None,
) -> list[str]:
    return ["DiscoverVersion"]
