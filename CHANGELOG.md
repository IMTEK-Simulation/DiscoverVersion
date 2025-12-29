This file lists all changes to the code

v0.3.1 (29Dec25)
----------------

* BUG: Fixed CI workflow to use `DISCOVER_VERSION` environment variable when building

v0.3.0 (29Dec25)
----------------

* ENH: Added `DISCOVER_VERSION` environment variable override for CI/CD builds
* ENH: Added CLI module (`python -m DiscoverVersion`) for command-line version discovery
* ENH: Added `discover-version` command-line entry point
* ENH: Added `write_version_file()` and `write_plain_version_file()` functions for generating version files

v0.2.6 (27Sept24)
-----------------

* TST: Fixed internal version

v0.2.5 (27Sept24)
-----------------

* ENH: Add safe.directory '*' when calling git

v0.2.4 (27Jul24)
----------------

* BUG: Fixed hard-coded version info in tests

v0.2.3 (27Jul24)
----------------

* BUG: Fixed version discovery in submodules

v0.2.2 (25Jul24)
----------------

* MAINT: Check if `.git` directory exists before running git

v0.2.1 (22Mar24)
----------------

* MAINT: Also detect version if not in toplevel git directory

v0.2.0 (22Mar24)
----------------

* ENH: Pass file/directory name for git discovery

v0.1.9 (22Mar24)
----------------

* MAINT: Changed discovery order

* v0.1.8 (22Mar24)
----------------

* MAINT: Added discovery via PKG-INFO file

* v0.1.7 (22Mar24)
----------------

* BUG: Use __name__ for package name

v0.1.6 (22Mar24)
----------------

* BUG: Hard-code package name

v0.1.5 (22Mar24)
----------------

* MAINT: Debug print package name

v0.1.4 (22Mar24)
----------------

* BUG: Detect if we are inside flit build isolation

v0.1.3 (22Mar24)
----------------

* BUG: Need to ask importlib before git

v0.1.2 (22Mar24)
----------------

* MAINT: Allow discovery from submodule

v0.1.1 (22Mar24)
----------------

* MAINT: Try git before importlib
* TST: Added simple test

v0.1.0 (22Mar24)
----------------

* Initial release; adjusted version discovery code from SurfaceTopography