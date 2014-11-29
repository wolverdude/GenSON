jschemagen
**********

A powerful, user-friendly `JSON Schema`_ generator built in Python.

It generates a new schema from existing schemas and/or objects. The schema is naively generated, so as always, you'll want to give it a once-over to make sure it's right.

The generator follows three rules:

1. *Every* object that was used to generate the new schema must still validate.
2. *Any* object that is valid under *any* merged schema must still validate.
3. The generated schema should be as strict as possible given the first 2 rules.

The third rule is has limits. The generator does not generate any specific validations for values other than ``type``. If you need those, you'll have to add them yourself once you get the generated schema.


CLI tool
========

``bin/jschemagen.py`` is an executable that takes a simple JSON object from stdin and outputs a naïve schema for it. There are additional options for generating a single schema from multiple objects or modifying an existing schema. To see these options, run:

.. code-block:: bash
    $ bin/jschemagen.py --help


Schema Generator API
====================

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

* ``merge_arrays`` (default ``True``): Assume all array items share the same schema (as they should). The alternate behavior is to create a different schema for each item in every array.

``add_schema(schema)``
++++++++++++++++++++++

Merges in an existing schema.

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

Tests are written in ``unittest``. You can run them easily with the ``nose`` package.

.. code-block:: bash
    $ nosetests


.. _JSON schema: //json-schema.org/
