GenSON
======

**GenSON** is a powerful, user-friendly `JSON Schema`_ generator built in Python.

.. note::
    This is *not* the Python equivalent of the `Java Genson library`_. If you are coming from Java need to create JSON objects in Python, you want `Python's builtin json library`_.)

GenSON's core function is to take JSON objects and generate schemas that describe them, but it is unique in its ability to *merge* schemas. It was originally built to describe the common structure of a large number of JSON objects, and it uses its merging ability to generate a single schema from any number of JSON objects and/or schemas.

GenSON's schema builder follows these three rules:

1. *Every* object it is given must validate under the generated schema.
2. *Any* object that is valid under *any* schema it is given must also validate under the generated schema. (there is one glaring exception to this, detailed `below`_)
3. The generated schema should be as strict as possible given the first 2 rules.


JSON Schema Implementation
--------------------------

**GenSON** is compatible with JSON Schema Draft 4 and above.

It is important to note that GenSON uses only a subset of JSON Schema's capabilities. This is mainly because it doesn't know the specifics of your data model, and it tries to avoid guessing them. Its purpose is to generate the basic structure so that you can skip the boilerplate and focus on the details of the schema.

Currently, GenSON only deals with these keywords:

* ``"$schema"``
* ``"type"``
* ``"items"``
* ``"properties"``
* ``"patternProperties"``
* ``"required"``
* ``"anyOf"``

You should be aware that this limited vocabulary could cause GenSON to violate rules 1 and 2. If you feed it schemas with advanced keywords, it will just blindly pass them on to the final schema. Note that ``"$ref"`` and ``id`` are also not supported, so GenSON will not dereference linked nodes when building a schema.


Installation
------------

.. code-block:: bash

    $ pip install genson


CLI Tool
--------

The package includes a ``genson`` executable that allows you to access this functionality from the command line. For usage info, run with ``--help``:

.. code-block:: bash

    $ genson --help

.. code-block::

    usage: genson.py [-h] [-d DELIM] [-i SPACES] [-s SCHEMA] [-$ URI] ...

    Generate one, unified JSON Schema from one or more JSON objects and/or JSON
    Schemas. It's compatible with Draft 4 and above.

    positional arguments:
      object                files containing JSON objects (defaults to stdin if no
                            arguments are passed)

    optional arguments:
      -h, --help            show this help message and exit
      -d DELIM, --delimiter DELIM
                            set a delimiter - Use this option if the input files
                            contain multiple JSON objects/schemas. You can pass
                            any string. A few cases ('newline', 'tab', 'space')
                            will get converted to a whitespace character. If this
                            option is omitted, the parser will try to auto-detect
                            boundaries
      -i SPACES, --indent SPACES
                            pretty-print the output, indenting SPACES spaces
      -s SCHEMA, --schema SCHEMA
                            file containing a JSON Schema (can be specified
                            multiple times to merge schemas)
      -$ URI, --schema-uri URI
                            the value of the '$schema' keyword (defaults to
                            'http://json-schema.org/schema#' or can be specified
                            in a schema with the -s option). If 'NULL' is passed,
                            the "$schema" keyword will not be included in the
                            result.

GenSON Python API
-----------------

``SchemaBuilder`` is the basic schema generator class. ``SchemaBuilder`` instances can be loaded up with existing schemas and objects before being serialized.

.. code-block:: python

    >>> from genson import SchemaBuilder

    >>> builder = SchemaBuilder()
    >>> builder.add_schema({"type": "object", "properties": {}})
    >>> builder.add_object({"hi": "there"})
    >>> builder.add_object({"hi": 5})

    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#',
     'type': 'object',
     'properties': {
        'hi': {'type': ['integer', 'string']}},
        'required': ['hi']}

    >>> print(builder.to_json(indent=2))
    {
      "$schema": "http://json-schema.org/schema#",
      "type": "object",
      "properties": {
        "hi": {
          "type": [
            "integer",
            "string"
          ]
        }
      },
      "required": [
        "hi"
      ]
    }

SchemaBuilder.__init__(schema_uri=None)
+++++++++++++++++++++++++++++++++++++++

:param schema_uri: value of the ``$schema`` keyword. If not given, it will use the value of the first available ``$schema`` keyword on an added schema or else the default: ``'http://json-schema.org/schema#'``. A value of ``False`` or ``None`` will direct GenSON to leave out the ``"$schema"`` keyword.

SchemaBuilder.add_schema(schema)
++++++++++++++++++++++++++++++++

Merge in a JSON schema. This can be a ``dict`` or another ``SchemaBuilder``

:param schema: a JSON Schema

.. note::
    There is no schema validation. If you pass in a bad schema,
    you might get back a bad schema.

SchemaBuilder.add_object(obj)
+++++++++++++++++++++++++++++

Modify the schema to accomodate an object.

:param obj: any object or scalar that can be serialized in JSON

SchemaBuilder.to_schema()
+++++++++++++++++++++++++

Generate a schema based on previous inputs.

:rtype: ``dict``

SchemaBuilder.to_json()
+++++++++++++++++++++++

Generate a schema and convert it directly to serialized JSON.

:rtype: ``str``

SchemaBuilder.__eq__(other)
+++++++++++++++++++++++++++

Check for equality with another ``SchemaBuilder`` object.

:param other: another ``SchemaBuilder`` object. Other types are accepted, but will always return ``False``

SchemaBuilder object interaction
++++++++++++++++++++++++++++++++

``SchemaBuilder`` objects can also interact with each other:

* You can pass one schema directly to another to merge them.
* You can compare schema equality directly.

.. code-block:: python

    >>> from genson import SchemaBuilder

    >>> b1 = SchemaBuilder()
    >>> b1.add_schema({"type": "object", "properties": {
    ...   "hi": {"type": "string"}}})
    >>> b2 = SchemaBuilder()
    >>> b2.add_schema({"type": "object", "properties": {
    ...   "hi": {"type": "integer"}}})
    >>> b1 == b2
    False

    >>> b1.add_schema(b2)
    >>> b2.add_schema(b1)
    >>> b1 == b2
    True
    >>> b1.to_schema()
    {'$schema': 'http://json-schema.org/schema#',
     'type': 'object',
     'properties': {'hi': {'type': ['integer', 'string']}}}


Seed Schemas
------------

There are several cases where multiple valid schemas could be generated from the same object. GenSON makes a default choice in all these ambiguous cases, but if you want it to choose differently, you can tell it what to do using a *seed schema*.

Seeding Arrays
++++++++++++++

For example, suppose you have a simple array with two items:

.. code-block:: python

    ['one', 1]

There are always two ways for GenSON to interpret any array: List and Tuple. Lists have one schema for every item, whereas Tuples have a different schema for every array position. This is analogous to the (now deprecated) ``merge_arrays`` option from version 0. You can read more about JSON Schema `array validation here`_.

List Validation
^^^^^^^^^^^^^^^

.. code-block:: json

    {
      "type": "array",
      "items": {"type": ["integer", "string"]}
    }

Tuple Validation
^^^^^^^^^^^^^^^^

.. code-block:: json

    {
      "type": "array",
      "items": [{"type": "integer"}, {"type": "string"}]
    }

By default, GenSON always interprets arrays using list validation, but you can tell it to use tuple validation by seeding it with a schema.

.. code-block:: python

    >>> from genson import SchemaBuilder

    >>> builder = SchemaBuilder()
    >>> builder.add_object(['one', 1])
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#',
     'type': 'array',
     'items': {'type': ['integer', 'string']}}

    >>> builder = SchemaBuilder()
    >>> seed_schema = {'type': 'array', 'items': []}
    >>> builder.add_schema(seed_schema)
    >>> builder.add_object(['one', 1])
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#',
     'type': 'array',
     'items': [{'type': 'string'}, {'type': 'integer'}]}

Note that in this case, the seed schema is actually invalid. You can't have an empty array as the value for an ``items`` keyword. But GenSON is a generator, not a validator, so you can fudge a little. GenSON will modify the generated schema so that it is valid, provided that there aren't invalid keywords beyond the ones it knows about.

Seeding patternProperties
+++++++++++++++++++++++++

Support for patternProperties_ is new in version 1; however, since GenSON's default behavior is to only use ``properties``, this powerful keyword can only be utilized with seed schemas. You will need to supply an ``object`` schema with a ``patternProperties`` object whose keys are RegEx strings. Again, you can fudge here and set the values to null instead of creating valid subschemas.

.. code-block:: python

    >>> from genson import SchemaBuilder

    >>> builder = SchemaBuilder()
    >>> builder.add_schema({'type': 'object', 'patternProperties': {r'^\d+$': None}})
    >>> builder.add_object({'1': 1, '2': 2, '3': 3})
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#', 'type': 'object', 'patternProperties':  {'^\\d+$': {'type': 'integer'}}}

There are a few gotchas you should be aware of here:

* GenSON is written in Python, so it uses the `Python flavor of RegEx`_.
* GenSON still prefers ``properties`` to ``patternProperties`` if a property already exists that matches one of your patterns, the normal property will be updated, *not* the pattern property.
* If a key matches multiple patterns, there is *no guarantee* of which one will be updated.
* The patternProperties_ docs themselves have some more useful pointers that can save you time.

Typeless Schemas
++++++++++++++++

In version 0, GenSON did not accept a schema without a type, but in order to be flexible in the support of seed schemas, support was added for version 1. However, GenSON violates rule #2 in its handling of typeless schemas. Any object will validate under an empty schema, but GenSON incorporates typeless schemas into the first-available typed schema, and since typed schemas are stricter than typless ones, so objects that would validate under an added schema will not validate under the result.

Compatibility
-------------

GenSON has been tested and verified using the following versions of Python:

* Python 2.7.11
* Python 3.3.5
* Python 3.4.4
* Python 3.5.1
* Python 3.6.2


Contributing
------------

When contributing, please follow these steps:

1. Clone the repo and make your changes.
2. Make sure your code has test cases written against it.
3. Make sure all the tests pass.
4. Lint your code with `Flake8`_.
5. Ensure the docs are accurate.
6. Add your name to the list of contributers.
7. Submit a Pull Request.

Tests
+++++

Tests are written in ``unittest``. You can run them all easily with the included executable ``bin/test.py``.

.. code-block:: bash

    $ bin/test.py

You can also invoke individual test suites:

.. code-block:: bash

    $ bin/test.py --test-suite test.test_gen_single


Potential Future Features
+++++++++++++++++++++++++

The following are extra features under consideration.

* recognize every validation keyword and ignore any that don't apply
* open up generator API for custom schema generator classes
* option to set error level
* custom serializer plugins
* logical support for more keywords:

  * ``enum``
  * ``min``/``max``
  * ``minLength``/``maxLength``
  * ``minItems``/``maxItems``
  * ``minProperties``/``maxProperties``
  * ``additionalItems``
  * ``additionalProperties``
  * ``format`` & ``pattern``
  * ``$ref`` & ``id``

.. _JSON Schema: http://json-schema.org/
.. _Java Genson library: https://owlike.github.io/genson/
.. _Python's builtin json library: https://docs.python.org/library/json.html
.. _Flake8: https://pypi.python.org/pypi/flake8
.. _below: #typeless-schemas
.. _array validation here: https://spacetelescope.github.io/understanding-json-schema/reference/array.html#items
.. _patternProperties: https://spacetelescope.github.io/understanding-json-schema/reference/object.html#pattern-properties
.. _`Python flavor of RegEx`: https://docs.python.org/3.6/library/re.html
