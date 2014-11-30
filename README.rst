GenSON
======

**GenSON** (rhymes with *Gen Con*) is a powerful, user-friendly `JSON Schema`_ generator built in Python.

Its power comes from the ability to generate a single schema from multiple objects. You can also throw existing schemas into the mix. Basically, you can feed it as many schemas and objects as you want and it will spit out one, unified schema for them all.

The generator follows these three rules:

1. *Every* object it is given must validate under the generated schema.
2. *Any* object that is valid under *any* schema it is given must also validate under the generated schema.
3. The generated schema should be as strict as possible given the first 2 rules.


JSON Schema Implementation
--------------------------

**GenSON** is a `Draft 4`_ generator. `Draft 3`_ support may come in the future.

It is important to note that the generator uses only a small subset of JSON Schema's capabilities. This is mainly because the generator doesn't know the specifics of your data model, and it doesn't try to guess them. Its purpose is to generate the basic structure so that you can skip the boilerplate and focus on the details of the schema.

This means that headers and most keywords aren't dealt with. Specifically, the generator only deals with 4 keywords: ``"type"``, ``"items"``, ``"properties"`` and ``"required"``. You should be aware that this limited vocabulary could cause the generator to violate rules 1 and 2. If you feed it schemas with advanced keywords, it will just blindly pass them on to the final schema.


CLI Tool
--------

The package includes a ``genson`` executable that allows you to access this functionality from the command line. For usage info, run with ``--help``:

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
                            mutliple times to merge schemas)


GenSON Python API
-----------------

``Schema`` is the basic schema generator class. ``Schema`` objects can be loaded up with existing schemas and objects before being serialized.

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

* ``merge_arrays`` (default ``True``): Assume all items in an array share the same schema. The alternate behavior is to create a different schema for each item in an array, only consolidating identical ones.

``add_schema(schema)``
^^^^^^^^^^^^^^^^^^^^^^

Merges in an existing schema. Take care here because there is no schema validation. If you pass in a bad schema, you'll get back a bad schema.

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


Tests
-----

Tests are written in ``unittest``. You can run them all easily with the included executable ``bin/test.py``.

.. code-block:: bash

    $ bin/test.py

You can also run any test file directly:

.. code-block:: bash

    $ python test/test_gen_single.py


TODO
----

* Validation for add_schema
* Headers
* Support for JSON Schema Draft 3


.. _JSON Schema: http://json-schema.org/
.. _Draft 4: http://json-schema.org/draft-04/schema#
.. _Draft 3: http://json-schema.org/draft-03/schema#
