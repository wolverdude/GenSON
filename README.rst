.. image:: https://travis-ci.com/wolverdude/GenSON.svg?branch=master
   :alt: Travis CI build badge
   :target: `Travis CI`_

GenSON
======

**GenSON** is a powerful, user-friendly `JSON Schema`_ generator built in Python.

.. note::
    This is *not* the Python equivalent of the `Java Genson library`_. If you are coming from Java and need to create JSON objects in Python, you want `Python's builtin json library`_.)

GenSON's core function is to take JSON objects and generate schemas that describe them, but it is unique in its ability to *merge* schemas. It was originally built to describe the common structure of a large number of JSON objects, and it uses its merging ability to generate a single schema from any number of JSON objects and/or schemas.

GenSON's schema builder follows these three rules:

1. *Every* object it is given must validate under the generated schema.
2. *Any* object that is valid under *any* schema it is given must also validate under the generated schema. (there is one glaring exception to this, detailed `below`_)
3. The generated schema should be as strict as possible given the first 2 rules.


JSON Schema Implementation
--------------------------

**GenSON** is compatible with JSON Schema Draft 6 and above.

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

    usage: genson [-h] [--version] [-d DELIM] [-e ENCODING] [-i SPACES]
                  [-s SCHEMA] [-$ SCHEMA_URI]
                  ...

    Generate one, unified JSON Schema from one or more JSON objects and/or JSON
    Schemas. Compatible with JSON-Schema Draft 4 and above.

    positional arguments:
      object                Files containing JSON objects (defaults to stdin if no
                            arguments are passed).

    optional arguments:
      -h, --help            Show this help message and exit.
      --version             Show version number and exit.
      -d DELIM, --delimiter DELIM
                            Set a delimiter. Use this option if the input files
                            contain multiple JSON objects/schemas. You can pass
                            any string. A few cases ('newline', 'tab', 'space')
                            will get converted to a whitespace character. If this
                            option is omitted, the parser will try to auto-detect
                            boundaries.
      -e ENCODING, --encoding ENCODING
                            Use ENCODING instead of the default system encoding
                            when reading files. ENCODING must be a valid codec
                            name or alias.
      -i SPACES, --indent SPACES
                            Pretty-print the output, indenting SPACES spaces.
      -s SCHEMA, --schema SCHEMA
                            File containing a JSON Schema (can be specified
                            multiple times to merge schemas).
      -$ SCHEMA_URI, --schema-uri SCHEMA_URI
                            The value of the '$schema' keyword (defaults to
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

``SchemaBuilder`` API
+++++++++++++++++++++

``__init__(schema_uri=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:param schema_uri: value of the ``$schema`` keyword. If not given, it will use the value of the first available ``$schema`` keyword on an added schema or else the default: ``'http://json-schema.org/schema#'``. A value of ``False`` or ``None`` will direct GenSON to leave out the ``"$schema"`` keyword.

``add_schema(schema)``
^^^^^^^^^^^^^^^^^^^^^^

Merge in a JSON schema. This can be a ``dict`` or another ``SchemaBuilder`` object.

:param schema: a JSON Schema

.. note::
    There is no schema validation. If you pass in a bad schema,
    you might get back a bad schema.

``add_object(obj)``
^^^^^^^^^^^^^^^^^^^

Modify the schema to accommodate an object.

:param obj: any object or scalar that can be serialized in JSON

``to_schema()``
^^^^^^^^^^^^^^^

Generate a schema based on previous inputs.

:rtype: ``dict``

``to_json()``
^^^^^^^^^^^^^

Generate a schema and convert it directly to serialized JSON.

:rtype: ``str``

``__eq__(other)``
^^^^^^^^^^^^^^^^^

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

In version 0, GenSON did not accept a schema without a type, but in order to be flexible in the support of seed schemas, support was added for version 1. However, GenSON violates rule #2 in its handling of typeless schemas. Any object will validate under an empty schema, but GenSON incorporates typeless schemas into the first-available typed schema, and since typed schemas are stricter than typless ones, objects that would validate under an added schema will not validate under the result.


Customizing ``SchemaBuilder``
-----------------------------

You can extend the ``SchemaBuilder`` class to add in your own logic (e.g. recording ``minimum`` and ``maximum`` for a number). In order to do this, you need to:

1. Create a custom ``SchemaStrategy`` class.
2. Create a ``SchemaBuilder`` subclass that includes your custom ``SchemaStrategy`` class(es).
3. Use your custom ``SchemaBuilder`` just like you would the stock ``SchemaBuilder``.

``SchemaStrategy`` Classes
++++++++++++++++++++++++++

GenSON uses the Strategy Pattern to parse, update, and serialize different kinds of schemas that behave in different ways. There are several ``SchemaStrategy`` classes that roughly correspond to different schema types. GenSON maps each node in an object or schema to an instance of one of these classes. Each instance stores the current schema state and updates or returns it when required.

You can modify the specific ways these classes work by extending them. You can inherit from any existing ``SchemaStrategy`` class, though ``SchemaStrategy`` and ``TypedSchemaStrategy`` are the most useful base classes. You should call ``super`` and pass along all arguments when overriding any instance methods.

The documentation below explains the public API and what you need to extend and override at a high level. Feel free to explore `the code`_ to see more, but know that the public API is documented here, and anything else you depend on could be subject to change. All ``SchemaStrategy`` subclasses maintain the public API though, so you can extend any of them in this way.

``SchemaStrategy`` API
++++++++++++++++++++++

[class constant] ``KEYWORDS``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This should be a tuple listing all of the JSON-schema keywords that this strategy knows how to handle. Any keywords encountered in added schemas will be be naively passed on to the generated schema unless they are in this list (or you override that behavior in ``to_schema``).

When adding keywords to a new ``SchemaStrategy``, it's best to splat the parent class's ``KEYWORDS`` into the new tuple.

[class method] ``match_schema(cls, schema)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return ``true`` if this strategy should be used to handle the passed-in schema.

:param schema: a JSON Schema in ``dict`` form
:rtype: ``bool``

[class method] ``match_object(cls, obj)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return ``true`` if this strategy should be used to handle the passed-in object.

:param obj: any object or scalar that can be serialized in JSON
:rtype: ``bool``

``__init__(self, node_class)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Override this method if you need to initialize an instance variable.

:param node_class: This param is not part of the public API. Pass it along to ``super``.

``add_schema(self, schema)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Override this to modify how a schema is parsed and stored.

:param schema: a JSON Schema in ``dict`` form

``add_object(self, obj)``
^^^^^^^^^^^^^^^^^^^^^^^^^

Override this to change the way a schemas are inferred from objects.

:param obj: any object or scalar that can be serialized in JSON

``to_schema(self)``
^^^^^^^^^^^^^^^^^^^

Override this method to customize how a schema object is constructed from the inputs. It is suggested that you invoke ``super`` as the basis for the return value, but it is not required.

:rtype: ``dict``

.. note::
    There is no schema validation. If you return a bad schema from this method,
    ``SchemaBuilder`` will output a bad schema.

``__eq__(self, other)``
^^^^^^^^^^^^^^^^^^^^^^^

When checking for ``SchemaBuilder`` equality, strategies are matched using ``__eq__``. The default implementation uses a simple ``__dict__`` equality check.

Override this method if you need to override that behavior. This may be useful if you add instance variables that aren't relevant to whether two SchemaStrategies are considered equal.

:rtype: ``bool``

``TypedSchemaStrategy`` API
+++++++++++++++++++++++++++

This is an abstract schema strategy for making simple schemas that only deal with the ``type`` keyword, but you can extend it to add more functionality. Subclasses must define the following two class constants, but you get the entire ``SchemaStrategy`` interface for free.

[class constant] ``JS_TYPE``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will be the value of the ``type`` keyword in the generated schema. It is also used to match any added schemas.


[class constant] ``PYTHON_TYPE``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a Python type or tuple of types that will be matched against an added object using ``isinstance``.

Extending ``SchemaBuilder``
+++++++++++++++++++++++++++

Once you have extended ``SchemaStrategy`` types, you'll need to create a ``SchemaBuilder`` class that uses them, since the default ``SchemaBuilder`` only incorporates the default strategies. To do this, extend the ``SchemaBuilder`` class and define one of these two constants inside it:

[class constant] ``EXTRA_STRATEGIES``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the standard (and suggested) way to add strategies. Set it to a tuple of all your new strategies, and they will be added to the existing list of strategies to check. This preserves all the existing functionality.

Note that order matters. GenSON checks the list in order, so the first strategy has priority over the second and so on. All ``EXTRA_STRATEGIES`` have priority over the default strategies.

[class constant] ``STRATEGIES``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This clobbers the existing list of strategies and completely replaces it. Set it to a tuple just like for ``EXTRA_STRATEGIES``, but note that if any object or schema gets added that your exhaustive list of strategies doesn't know how to handle, you'll get an error. You should avoid doing this unless you're extending most or all existing strategies in some way.

Example: ``MinNumber``
++++++++++++++++++++++

Here's some example code creating a number strategy that tracks the `minimum number`_ seen and includes it in the output schema.

.. code-block:: python

    from genson import SchemaBuilder
    from genson.schema.strategies import Number

    class MinNumber(Number):
        # add 'minimum' to list of keywords
        KEYWORDS = (*Number.KEYWORDS, 'minimum')

        # create a new instance variable
        def __init__(self, node_class):
            super().__init__(node_class)
            self.min = None

        # capture 'minimum's from schemas
        def add_schema(self, schema):
            super().add_schema(schema)
            if self.min is None:
                self.min = schema.get('minimum')
            elif 'minimum' in schema:
                self.min = min(self.min, schema['minimum'])

        # adjust minimum based on the data
        def add_object(self, obj):
            super().add_object(obj)
            self.min = obj if self.min is None else min(self.min, obj)

        # include 'minimum' in the output
        def to_schema(self):
            schema = super().to_schema()
            schema['minimum'] = self.min
            return schema

    # new SchemaBuilder class that uses the MinNumber strategy in addition
    # to the existing strategies. Both MinNumber and Number are active, but
    # MinNumber has priority, so it effectively replaces Number.
    class MinNumberSchemaBuilder(SchemaBuilder):
        """ all number nodes include minimum """
        EXTRA_STRATEGIES = (MinNumber,)

    # this class *ONLY* has the MinNumber strategy. Any object that is not
    # a number will cause an error.
    class ExclusiveMinNumberSchemaBuilder(SchemaBuilder):
        """ all number nodes include minimum, and only handles number """
        STRATEGIES = (MinNumber,)

Now that we have the MinNumberSchemaBuilder class, let's see how it works.

.. code-block:: python

    >>> builder = MinNumberSchemaBuilder()
    >>> builder.add_object(5)
    >>> builder.add_object(7)
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#', 'type': 'integer', 'minimum': 5}
    >>> builder.add_object(-2)
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#', 'type': 'integer', 'minimum': -2}
    >>> builder.add_schema({'$schema': 'http://json-schema.org/schema#', 'type': 'integer', 'minimum': -7})
    >>> builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#', 'type': 'integer', 'minimum': -7}

Note that the exclusive builder is much more particular.

.. code-block:: python

    >>> builder = MinNumberSchemaBuilder()
    >>> picky_builder = ExclusiveMinNumberSchemaBuilder()
    >>> picky_builder.add_object(5)
    >>> picky_builder.to_schema()
    {'$schema': 'http://json-schema.org/schema#', 'type': 'integer', 'minimum': 5}
    >>> builder.add_object(None) # this is fine
    >>> picky_builder.add_object(None) # this fails
    genson.schema.node.SchemaGenerationError: Could not find matching schema type for object: None


Contributing
------------

When contributing, please follow these steps:

1. Clone the repo and make your changes.
2. Make sure your code has test cases written against it.
3. Lint your code with `Flake8`_.
4. Run `tox`_ to make sure the test suite passes.
5. Ensure the docs are accurate.
6. Add your name to the list of contributers.
7. Submit a Pull Request.

Tests
+++++

Tests are written in ``unittest`` and are run using `tox`_ and `nose`_. Tox will run all tests with coverage against each supported Python version that is installed on your machine.

.. code-block:: bash

    $ tox

Integration
+++++++++++

When you submit a PR, `Travis CI`_ performs the following steps:

1. Lints the code with Flake8
2. Runs the entire test suite against each supported Python version.
3. Ensures that test coverage is at least 90%

If any of these steps fail, your PR cannot be merged until it is fixed.

Potential Future Features
+++++++++++++++++++++++++

The following are extra features under consideration.

* recognize every validation keyword and ignore any that don't apply
* option to set error level
* custom serializer plugins
* logical support for more keywords:

  * ``enum``
  * ``minimum``/``maximum``
  * ``minLength``/``maxLength``
  * ``minItems``/``maxItems``
  * ``minProperties``/``maxProperties``
  * ``additionalItems``
  * ``additionalProperties``
  * ``format`` & ``pattern``
  * ``$ref`` & ``id``

.. _JSON Schema: http://json-schema.org/
.. _Java Genson library: https://owlike.github.io/genson/
.. _`Python's builtin json library`: https://docs.python.org/library/json.html
.. _below: #typeless-schemas
.. _array validation here: https://spacetelescope.github.io/understanding-json-schema/reference/array.html#items
.. _patternProperties: https://spacetelescope.github.io/understanding-json-schema/reference/object.html#pattern-properties
.. _Python flavor of RegEx: https://docs.python.org/3.6/library/re.html
.. _the code: https://github.com/wolverdude/GenSON/tree/master/genson/schema/strategies
.. _minimum number: https://json-schema.org/understanding-json-schema/reference/numeric.html#range
.. _Flake8: https://pypi.python.org/pypi/flake8
.. _tox: https://pypi.python.org/pypi/tox
.. _nose: https://pypi.python.org/pypi/nose
.. _Travis CI: https://travis-ci.com/github/wolverdude/GenSON
