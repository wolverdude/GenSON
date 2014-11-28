import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='jschemagen',
    version='0.1.0',
    description='A powerful, user-friendly JSON Schema generator.',
    long_description=(read('README.md')),
    url='http://github.com/wolverdude/jschemagen/',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton (dot) jr (at) gmail (dot) com',
    # ^^^ Much like Mrs. Bun, I don't like spam.
    py_modules=['jschemagen'],
    include_package_data=True,
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
