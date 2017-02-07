#!/usr/bin/env python
from setuptools import setup
from re import sub


def get_long_docs(*filenames):
    """Build rst description from a set of files."""
    docs = []
    for filename in filenames:
        with open(filename, 'r') as f:
            docs.append(f.read())

    return pypi_safe("\n\n".join(docs))


def pypi_safe(rst):
    """ PyPI is using an unpatched version of Python that doesn't like
        code-block directives: http://bugs.python.org/issue23063 """
    return sub('\.\. code-block::.*\n', '::\n', rst)


setup(
    name='genson',
    version='0.2.1',
    description='GenSON is a powerful, user-friendly JSON Schema generator.',
    long_description=get_long_docs('README.rst', 'HISTORY.rst', 'AUTHORS.rst'),
    keywords=['json', 'schema', 'object', 'generate', 'generator', 'builder',
              'draft 4', 'validate', 'validation'],
    url='https://github.com/wolverdude/genson/',
    download_url='https://github.com/wolverdude/GenSON/tarball/v0.2s.0',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton' '.' 'jr' '@' 'gmail' '.' 'com',
    # ^^^ Much like Mrs. Bun, I don't like spam.
    packages=['genson'],
    include_package_data=True,
    entry_points={'console_scripts': ['genson = genson.genson:main']},
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    tests_require=[
        'jsonschema>=2.5.1',
    ],
    test_suite='test',
)
