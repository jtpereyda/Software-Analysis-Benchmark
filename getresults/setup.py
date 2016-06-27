#!/usr/bin/env python

# Copyright (C) 2015 Schweitzer Engineering Laboratories, Inc.

import ast
import os
import re

from setuptools import setup, find_packages

setup_dir = os.path.abspath(os.path.dirname(__file__))


# Project-specific settings:
NAME = 'getresults'
DESCRIPTION = 'Parse expected Toyota Benchmark analysis results and compare.'
VERSION_FILE_PATH = ['getresults', '__init__.py']
EXCLUDE_PACKAGES = []
INSTALL_REQUIRES = ['tabulate', 'typing', 'requests', 'cached_property']
EXTRAS_REQUIRE = {
    # This list is duplicated in tox.ini. Make sure to change both!
    # This can stop once tox supports installing package extras.
    'dev': ['mock', 'pytest'],
}


# Boilerplate:
def find_version(*path_elements):
    """Search a file for `__version__ = 'version number'` and return version.

    @param path_elements: Arguments specifying file to search.

    @return: Version number string.
    """
    path = os.path.join(setup_dir, *path_elements)
    for line in open(path):
        for match in re.finditer(r'__version__\s*=\s(.*)$', line):
            return ast.literal_eval(match.group(1))
    raise RuntimeError("version string not found in {0}".format(path))


def main():
    setup(
        name=NAME,
        version=find_version(*VERSION_FILE_PATH),
        description=DESCRIPTION,
        packages=find_packages(exclude=EXCLUDE_PACKAGES),
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
    )

if __name__ == '__main__':
    main()
