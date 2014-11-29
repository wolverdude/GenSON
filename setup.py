from setuptools import setup, find_packages


def get_long_docs(*filenames):
    """Build rst description from a set of markdown files."""
    docs = []
    for filename in filenames:
        with open(filename, 'r') as f:
            docs.append(f.read())

    return "\n\n".join(docs)


setup(
    name='jschemagen',
    version='0.1.0',
    description='A powerful, user-friendly JSON Schema generator.',
    long_description=get_long_docs('README.rst', 'HISTORY.rst', 'AUTHORS.rst'),
    url='https://github.com/wolverdude/jschemagen/',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton (dot) jr (at) gmail (dot) com',
    # ^^^ Much like Mrs. Bun, I don't like spam.
    py_modules=['jschemagen'],
    packages=find_packages(exclude="test"),
    include_package_data=True,
    entry_points={
        'console_scripts': ['jschemagen = jschemagen.jschemagen:main']},
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
    ],
)
