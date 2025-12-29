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
Command-line interface for DiscoverVersion.

Usage:
    python -m DiscoverVersion [options] [path]

Examples:
    # Print version for current directory
    python -m DiscoverVersion

    # Print version for specific path
    python -m DiscoverVersion /path/to/project

    # Write version to a Python file
    python -m DiscoverVersion --write-to _version.py

    # Write version to a plain text file (for Meson)
    python -m DiscoverVersion --write-to VERSION --plain
"""

import argparse
import sys

from .Discovery import (
    CannotDiscoverVersion,
    get_version_from_env,
    get_version_from_git,
    get_version_from_pkginfo,
    write_version_file,
    write_plain_version_file,
)


def main():
    parser = argparse.ArgumentParser(
        description="Discover and output package version from git or PKG-INFO.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m DiscoverVersion                     Print version for current directory
  python -m DiscoverVersion /path/to/project    Print version for specific path
  python -m DiscoverVersion --write-to _version.py    Write Python version file
  python -m DiscoverVersion --write-to VERSION --plain    Write plain text version
        """,
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the project directory (default: current directory)",
    )
    parser.add_argument(
        "--write-to",
        metavar="FILE",
        help="Write version to a file instead of printing",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Write plain text file (just version string) instead of Python file",
    )
    parser.add_argument(
        "--fallback",
        metavar="VERSION",
        default="0.0.0",
        help="Fallback version if discovery fails (default: 0.0.0)",
    )
    parser.add_argument(
        "--no-env",
        action="store_true",
        help="Don't check DISCOVER_VERSION environment variable",
    )
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Don't try to discover version from git",
    )
    parser.add_argument(
        "--no-pkginfo",
        action="store_true",
        help="Don't try to discover version from PKG-INFO",
    )

    args = parser.parse_args()

    version = None
    tried = []

    # Try environment variable first
    if not args.no_env:
        tried.append("env")
        version = get_version_from_env()

    # Try PKG-INFO
    if version is None and not args.no_pkginfo:
        tried.append("PKG-INFO")
        try:
            version = get_version_from_pkginfo()
        except CannotDiscoverVersion:
            pass

    # Try git
    if version is None and not args.no_git:
        tried.append("git")
        try:
            version = get_version_from_git(args.path)
        except CannotDiscoverVersion:
            pass

    # Use fallback if nothing worked
    if version is None:
        version = args.fallback
        if args.fallback == "0.0.0":
            print(
                f"Warning: Could not discover version (tried: {', '.join(tried)}), "
                f"using fallback: {args.fallback}",
                file=sys.stderr,
            )

    # Output the version
    if args.write_to:
        if args.plain:
            write_plain_version_file(version, args.write_to)
        else:
            write_version_file(version, args.write_to)
        print(f"Wrote version {version} to {args.write_to}", file=sys.stderr)
    else:
        print(version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
