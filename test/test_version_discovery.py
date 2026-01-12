#
# Copyright 2021 Lars Pastewka
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
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
Tests version discovery functionality.
"""

import os
import subprocess
from tempfile import TemporaryDirectory

from DiscoverVersion import __version__, get_version


_current_version = "0.4.0"


def test_version_discovery():
    assert __version__.startswith(_current_version)


def test_version_from_nested_module():
    assert get_version("DiscoverVersion", __file__).startswith(_current_version)

    assert get_version("DiscoverVersion", __file__, use_git=False).startswith(
        _current_version
    )


def test_version_from_git_submodule():
    with TemporaryDirectory() as tmpdir:
        # Create git repository
        os.mkdir(f"{tmpdir}/my-git-repository")
        r = subprocess.run(
            ["git", "init"], cwd=f"{tmpdir}/my-git-repository", stdout=subprocess.PIPE
        )
        assert r.returncode == 0
        # Create and add git submodule
        assert r.returncode == 0
        r = subprocess.run(
            [
                "git",
                "submodule",
                "add",
                "https://github.com/IMTEK-Simulation/DiscoverVersion.git",
            ],
            cwd=f"{tmpdir}/my-git-repository",
            stdout=subprocess.PIPE,
        )
        assert r.returncode == 0
        assert get_version(
            "DiscoverVersion",
            f"{tmpdir}/my-git-repository/DiscoverVersion",
            use_importlib=False,
            use_pkginfo=False,
        ).startswith(_current_version)
