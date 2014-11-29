jschemagen
**********

A powerful, user-friendly `JSON Schema`_ generator built in Python.

Its power comes from the ability to generate a single schema from multiple objects and merge in existing schemas as well. Basically, you can feed in as many schemas and objects as you want and it should generate one schema under which they are all valid.

The generator follows three rules:

1. *Every* object that was used to generate the new schema must still validate.
2. *Any* object that is valid under *any* merged schema must still validate.
3. The generated schema should be as strict as possible given the first 2 rules.


JSON Schema Implementation
==========================

This is a Draft 4 generator (``"$schema": "http://json-schema.org/draft-04/schema#"``"). Draft 3 support may come in the future. Even so, there are a couple of compliance issues.

The generator only deals with 4 keywords: ``"type"``, ``"items"``, ``"properties"`` and ``"required"``. This is mainly because the generator doesn't know the specifics of your data model. Its purpose is to generate the basic structure so that you can skip the boilerplate and focus on tweaking the schema.

You should be aware that this limited vocabulary could cause the generator to violate rules 1 and 2 if you feed it schemas with advanced keywords. It will just blindly pass them on into the final schema.

This also means that headers aren't included. This may change in the future, but for now, it's still manual.


CLI tool
========

The package includes a ``jschemagen`` executable that allows you to access this functionality from the command line. For usage info, run with ``--help``:

.. code-block:: bash

    $ jschemagen.py --help


jschemagen Python API
=====================

``Schema`` is the basic schema generator class. ``Schema`` objects can be loaded up with existing schemas and objects before being serialized.

.. code-block:: python

    import jschemagen

    s = jschemagen.Schema()
    s.add_schema({"type": "object", "properties": {}})
    s.add_object({"hi": "there"})
    s.add_object({"hi": 5})

    s.to_dict()
    #=> {"type": "object", "properties": {"hi": {"type": ["number", "string"]}}}

    s.to_json()
    #=> "{\"type\": \"object\", \"properties\": {\"hi\": {\"type\": [\"number\", \"string\"]}}}"


Schema Object Methods
---------------------

``Schema(merge_arrays=True)``
+++++++++++++++++++++++++++++

Builds a schema generator object.

arguments:

* ``merge_arrays`` (default ``True``): Assume all items in an array share the same schema. The alternate behavior is to create a different schema for each item in an array, only consolidating identical ones.

``add_schema(schema)``
++++++++++++++++++++++

Merges in an existing schema. Take care here because there is no schema validation. If you pass in a bad schema, you'll get back a bad schema.

arguments:

* ``schema`` (required - ``dict`` or ``Schema``): an existing JSON Schema to merge.

``add_object(obj)``
+++++++++++++++++++

Modify the schema to accomodate an object.

arguments:

* ``obj`` (required - ``dict``): a JSON object to use in generate the schema.

``to_dict()``
+++++++++++++

Convert the current schema to a ``dict``.

``to_json()``
+++++++++++++

Convert the current schema directly to serialized JSON.

Schema Object Interaction
-------------------------

Schema objects can also interact with each other:

* You can pass one schema directly to another to merge them.
* You can compare schema equality directly.

.. code-block:: python

    import jschemagen

    s1 = jschemagen.Schema()
    s1.add_schema({"type": "object", "properties": {"hi": {"type": "string"}}})

    s2 = jschemagen.Schema()
    s2.add_schema({"type": "object", "properties": {"hi": {"type": "number"}}})

    s1 == s2
    #=> False

    s1.add_schema(s2)
    s2.add_schema(s1)

    s1 == s2
    #=> True

    s1.to_dict()
    #=> {"type": "object", "properties": {"hi": {"type": ["number", "string"]}}}


Tests
=====

Tests are written in ``unittest``. You can run them all easily with the included executable ``bin/test.py``.

.. code-block:: bash

    $ bin/test.py

You can also run any test file directly:

.. code-block:: bash

    $ python test/test_gen_single.py


TODO
====

* Support for JSON Schema Draft 3
* Headers
* validation for add_schema


.. _JSON schema: //json-schema.org/
