#!/usr/bin/env python
import re
from setuptools import setup


def get_version():
    with open('genson/__init__.py') as f:
        match = re.search(r"__version__ = '([\d\.]+)'", f.read())
        return match.group(1)


def get_long_docs(*filenames):
    """Build rst description from a set of files."""
    docs = []
    for filename in filenames:
        with open(filename, 'r') as f:
            docs.append(f.read())

    return "\n\n".join(docs)


setup(
    name='genson',
    version=get_version(),
    description='GenSON is a powerful, user-friendly JSON Schema generator.',
    long_description=get_long_docs('README.rst', 'HISTORY.rst', 'AUTHORS.rst'),
    keywords=['json', 'schema', 'json-schema', 'jsonschema', 'object',
              'generate', 'generator', 'builder', 'merge',
              'draft 7', 'validate', 'validation'],
    url='https://github.com/wolverdude/genson/',
    download_url='https://github.com/wolverdude/GenSON/tarball/v0.2s.0',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton' '.' 'jr' '@' 'gmail' '.' 'com',
    packages=['genson'],
    include_package_data=True,
    entry_points={'console_scripts': ['genson = genson.cli:main']},
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
