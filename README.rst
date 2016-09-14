GenSON
======

**GenSON** is a powerful, user-friendly `JSON Schema`_ generator built
in Python.

(**Note**: This is not to be confused with the `Java Genson library`_.
If you are coming from Java and looking for a Python equivalent, this is
not it. You should instead look into `Python's builtin json library`_.)

Its power comes from the ability to generate a single schema from
multiple objects. You can also throw existing schemas into the mix.
Basically, you can feed it as many schemas and objects as you want and
it will spit out one, unified schema for them all.

The generator follows these three rules:

1. *Every* object it is given must validate under the generated schema.
2. *Any* object that is valid under *any* schema it is given must also
   validate under the generated schema.
3. The generated schema should be as strict as possible given the first
   2 rules.


JSON Schema Implementation
--------------------------

**GenSON** is a `Draft 4`_ generator.

It is important to note that the generator uses only a small subset of
JSON Schema's capabilities. This is mainly because the generator doesn't
know the specifics of your data model, and it doesn't try to guess them.
Its purpose is to generate the basic structure so that you can skip the
boilerplate and focus on the details of the schema.

This means that headers and most keywords aren't dealt with.
Specifically, the generator only deals with 4 keywords: ``"type"``,
``"items"``, ``"properties"`` and ``"required"``. You should be aware
that this limited vocabulary could cause the generator to violate rules
1 and 2. If you feed it schemas with advanced keywords, it will just
blindly pass them on to the final schema.


CLI Tool
--------

The package includes a ``genson`` executable that allows you to access
this functionality from the command line. For usage info, run with
``--help``:

.. code-block:: bash

    $ genson --help

.. code-block:: none

    usage: genson [-h] [-a] [-d DELIM] [-i SPACES] [-s SCHEMA] ...

    Generate one, unified JSON Schema from one or more JSON objects and/or JSON
    Schemas. (uses Draft 4 - http://json-schema.org/draft-04/schema)

    positional arguments:
      object                files containing JSON objects (defaults to stdin if no
                            arguments are passed and the -s option is not present)

    optional arguments:
      -h, --help            show this help message and exit
      -a, --no-merge-arrays
                            generate a different subschema for each element in an
                            array rather than merging them all into one
      -d DELIM, --delimiter DELIM
                            set a delimiter - Use this option if the input files
                            contain multiple JSON objects/schemas. You can pass
                            any string. A few cases ('newline', 'tab', 'space')
                            will get converted to a whitespace character, and if
                            empty string ('') is passed, the parser will try to
                            auto-detect where the boundary is.
      -i SPACES, --indent SPACES
                            pretty-print the output, indenting SPACES spaces
      -s SCHEMA, --schema SCHEMA
                            file containing a JSON Schema (can be specified
                            multiple times to merge schemas)


GenSON Python API
-----------------

``Schema`` is the basic schema generator class. ``Schema`` objects can
be loaded up with existing schemas and objects before being serialized.

.. code-block:: python

    import genson

    s = genson.Schema()
    s.add_schema({"type": "object", "properties": {}})
    s.add_object({"hi": "there"})
    s.add_object({"hi": 5})

    s.to_dict()
    #=> {"type": "object", "properties": {"hi": {"type": ["integer", "string"]}}}

    s.to_json()
    #=> "{\"type\": \"object\", \"properties\": {\"hi\": {\"type\": [\"integer\", \"string\"]}}}"


Schema Object Methods
+++++++++++++++++++++

``Schema(merge_arrays=True)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Builds a schema generator object.

arguments:

* `merge_arrays` (default `True`): Assume all array items share the same
  schema (as they should). The alternate behavior is to merge schemas
  based on position in the array.

``add_schema(schema)``
^^^^^^^^^^^^^^^^^^^^^^

Merges in an existing schema. Take care here because there is no schema
validation. If you pass in a bad schema, you'll get back a bad schema.

arguments:

* ``schema`` (required - ``dict`` or ``Schema``): an existing JSON Schema to merge.

``add_object(obj)``
^^^^^^^^^^^^^^^^^^^

Modify the schema to accommodate an object.

arguments:

* ``obj`` (required - ``dict``): a JSON object to use in generating the schema.

``to_dict()``
^^^^^^^^^^^^^

Convert the current schema to a ``dict``.

``to_json()``
^^^^^^^^^^^^^

Convert the current schema directly to serialized JSON.

Schema Object Interaction
+++++++++++++++++++++++++

Schema objects can also interact with each other:

* You can pass one schema directly to another to merge them.
* You can compare schema equality directly.

.. code-block:: python

    import genson

    s1 = genson.Schema()
    s1.add_schema({"type": "object", "properties": {"hi": {"type": "string"}}})

    s2 = genson.Schema()
    s2.add_schema({"type": "object", "properties": {"hi": {"type": "integer"}}})

    s1 == s2
    #=> False

    s1.add_schema(s2)
    s2.add_schema(s1)

    s1 == s2
    #=> True

    s1.to_dict()
    #=> {"type": "object", "properties": {"hi": {"type": ["integer", "string"]}}}


Compatibility
-------------

GenSON has been tested and verified using the following versions of Python:

* Python 2.7.11
* Python 3.3.5
* Python 3.4.4
* Python 3.5.1


Contributing
------------

When contributing, please follow these steps:

1. Clone the repo and make your changes.
2. Make sure your code has test cases written against it.
3. Make sure all the tests pass.
4. Lint your code with `Flake8`_.
5. Add your name to the list of contributers.
6. Submit a Pull Request.

Tests
+++++

Tests are written in ``unittest``. You can run them all easily with the
included executable ``bin/test.py``.

.. code-block:: bash

    $ bin/test.py

You can also invoke individual test suites:

.. code-block:: bash

    $ bin/test.py --test-suite test.test_gen_single


.. _JSON Schema: http://json-schema.org/
.. _Java Genson library: https://owlike.github.io/genson/
.. _Python's builtin json library: https://docs.python.org/library/json.html
.. _Draft 4: http://json-schema.org/draft-04/schema
.. _Flake8: https://pypi.python.org/pypi/flake8
