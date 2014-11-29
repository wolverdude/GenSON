try:
    import pypandoc
except (IOError, ImportError):
    raise ImportError(
        "pypandoc required for packaging because PyPI likes .rst and I don't.")

from setuptools import setup


def get_long_docs(*filenames):
    """Build rst description from a set of markdown files."""
    docs = []
    for filenames in filenames:
        docs.append(pypandoc.convert(filenames, 'rst'))

    return "\n\n".join(docs)


setup(
    name='jschemagen',
    version='0.1.0',
    description='A powerful, user-friendly JSON Schema generator.',
    long_description=get_long_docs('README.md'),
    url='http://github.com/wolverdude/jschemagen/',
    license='MIT',
    author='Jon Wolverton',
    author_email='wolverton (dot) jr (at) gmail (dot) com',
    # ^^^ Much like Mrs. Bun, I don't like spam.
    py_modules=['jschemagen'],
    include_package_data=True,
    entry_points={'console_scripts': ['jschemagen = bin.jschemagen:main']},
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
