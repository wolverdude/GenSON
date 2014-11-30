from setuptools import setup, find_packages


def get_long_docs(*filenames):
    """Build rst description from a set of markdown files."""
    docs = []
    for filename in filenames:
        with open(filename, 'r') as f:
            docs.append(f.read())

    return "\n\n".join(docs)


setup(
    name='genson',
    version='0.1.0',
    description='GenSON is a powerful, user-friendly JSON Schema generator.',
    long_description=get_long_docs('README.rst', 'HISTORY.rst', 'AUTHORS.rst'),
    keywords=['json', 'schema', 'object', 'generate', 'generator', 'builder',
              'draft 4', 'validate', 'validation'],
    url='https://github.com/wolverdude/genson/',
    download_url='https://github.com/wolverdude/GenSON/tarball/v0.1.0',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton' '.' 'jr' '@' 'gmail' '.' 'com',
    # ^^^ Much like Mrs. Bun, I don't like spam.
    py_modules=['genson'],
    packages=find_packages(exclude="test"),
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
