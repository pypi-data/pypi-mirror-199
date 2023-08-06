# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import codecs
from os import path
from setuptools import setup, find_packages
import re


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'airslate'
PKG_DIR = path.abspath(path.dirname(__file__))
META_PATH = path.join(PKG_DIR, PKG_NAME, '__init__.py')
META_CONTENTS = read_file(META_PATH)


def load_long_description():
    """Load long description from file README.rst."""
    def changes():
        changelog = path.join(PKG_DIR, 'CHANGELOG.rst')
        pat = r"(\d+.\d+.\d+ \(.*?\)\r?\n.*?)\r?\n\r?\n\r?\n----\r?\n\r?\n\r?\n"  # noqa: E501
        result = re.search(pat, read_file(changelog), re.S)

        return result.group(1) if result else ''

    try:
        title = f"{PKG_NAME}: {find_meta('description')}"
        head = '=' * len(title)

        contents = (
            head,
            format(title.strip(' .')),
            head,
            read_file(path.join(PKG_DIR, 'README.rst')).split(
                '.. teaser-begin'
            )[1],
            '',
            'Release Information',
            '===================\n',
            changes(),
            '',
            f"`Full changelog <{find_meta('url')}/blob/main/CHANGELOG.rst>`_.",
            '',
            '',
            read_file(path.join(PKG_DIR, 'AUTHORS.rst')),
        )

        return '\n'.join(contents)
    except (RuntimeError, FileNotFoundError) as read_error:
        message = 'Long description could not be read from README.rst'
        raise RuntimeError(f'{message}: {read_error}') from read_error


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440."""
    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS."""
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        f'Unable to find __{meta}__ string in package meta file')


def get_version_string():
    """Return package version as listed in `__version__` in meta file."""
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


# What does this project relate to.
KEYWORDS = [
    'airslate',
    'crm',
    'nocode',
    'addons',
    'bots',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',

    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
]

# Dependencies that are downloaded by pip on installation and why.
INSTALL_REQUIRES = [
    'requests>=2.20.0,==2.*',  # Interact with airSlate HTTP API
    'urllib3>=1.21.1,<1.27',  # Our internal HTTP client

]

DEPENDENCY_LINKS = []

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[testing,docs,develop]
#
EXTRAS_REQUIRE = {
    # Dependencies that are required to run tests
    'testing': [
        'pytest>=6.2.2',  # Our tests framework
        'pytest-cov>=2.11.1',  # Pytest plugin for measuring coverage
        'responses>=0.12.0',  # Mocking out the requests Python library
        'pylint>=2.6.0,!=2.6.1',  # Python code static checker
        'flake8>=3.8.4',  # The modular source code checker
    ],
    # Dependencies that are required to build documentation
    'docs': [],
}

# Dependencies that are required to develop package
DEVELOP_REQUIRE = [
    'twine>=3.3.0',  # Publishing packages on PyPI
    'setuptools>=53.0.0',  # Build and install packages
    'wheel>=0.36.2',  # A built-package format for Python
    'check-wheel-contents>=0.2.0',  # Check wheels have the right contents
]

EXTRAS_REQUIRE['develop'] = \
    DEVELOP_REQUIRE + EXTRAS_REQUIRE['testing'] + EXTRAS_REQUIRE['docs']

# Project's URLs
PROJECT_URLS = {
    'Changelog': f"{find_meta('url')}/blob/main/CHANGELOG.rst",
    'Bug Tracker': f"{find_meta('url')}/issues",
    'Source Code': find_meta('url'),
}

if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('author_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=load_long_description(),
        long_description_content_type='text/x-rst',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(exclude=['tests.*', 'tests']),
        platforms='any',
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.7, <4',
        install_requires=INSTALL_REQUIRES,
        dependency_links=DEPENDENCY_LINKS,
        extras_require=EXTRAS_REQUIRE,
    )
