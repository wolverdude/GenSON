History
=======

1.2.0
-----

* ``SchemaStrategies`` are now extendable, enabling custom ``SchemaBuilder`` classes.
* optimize ``__eq__`` logic

1.1.0
-----

* add support for Python 3.7
* drop support for Python 3.3
* drop support for JSON-Schema Draft 4 (because it doesn't allow empty ``required`` arrays)
* **Bugfix**: preserve empty ``required`` arrays (fixes #25)
* **Bugfix**: handle nested ``anyOf`` keywords (fixes #35)

1.0.2
-----

* add support for ``long`` integers in Python 2.7
* update test-skipping decorator to use standard version requirement strings

1.0.1
-----

* **Bugfix**: seeding an object schema with a ``"required"`` keyword caused an error
* **Docs**: fix mislabeled method

1.0.0
-----

This version was a total overhaul. The main change was to split Schema into three separate classes, making it simpler to add more complicated functionality by having different generator types to handle the different schema types.

1. ``SchemaNode`` to manage the tree structure
2. ``SchemaGenerator`` for the schema generation logic
3. ``SchemaBuilder`` to manage the public API

Interface Changes
+++++++++++++++++

* ``SchemaBuilder`` is the new ``Schema``
* ``to_dict()`` is now called ``to_schema()``

To make the transition easier, there is still a ``Schema`` class that wraps ``SchemaBuilder`` with a backwards-compatibility layer, but you will trigger a ``PendingDeprecationWarning`` if you use it.

Seed Schemas
++++++++++++

The ``merge_arrays`` option has been removed in favor of seed schemas. You can now seed specific nodes as list or tuple instead of setting a global option for every node in the schema tree.

You can also now seed object nodes with ``patternProperties``, which was a highly requested feature.

Other Changes
+++++++++++++

* include ``"$schema"`` keyword
* accept schemas without ``"type"`` keyword
* use ``"anyOf"`` keyword to help combine schemas
* add ``SchemaGenerationError`` for better error handling
* empty ``"properties"`` and ``"items"`` are not included in generated schemas
* ``genson`` executable

  * new ``--schema-uri`` option
  * auto-detect object boundaries by default

0.2.3
-----
* **Docs**: add installation instructions

0.2.2
-----
* **Docs**: Python 3.6 is now explicitly tested and listed as compatible.

0.2.1
-----
* **Bugfix**: ``add_schema`` failed when adding list-style array schemas
* **Bugfix**: typo in readme

0.2.0
-----

* **Bugfix**: Options were not propagated down to subschemas.
* **Bugfix**: Empty arrays resulted in invalid schemas because it still included an ``items`` property.
* **Bugfix**: ``items`` was being set to a list even when ``merge_arrays`` was set to ``True``. This resulted in overly permissive schemas because ``items`` are matched optionally by default.
* **Improvement**: Positional Array Matching - In order to be more consistent with the way JSON Schema works, the alternate to ``merge_arrays`` is no longer never to merge list items, but instead to merge them based on their position in the list.
* **Improvement**: Schema Incompatibility Warning - A schema incompatibility used to cause a fatal error with a nondescript warning. The message has been improved and it has been reduced to a warning.

0.1.0 (2014-11-29)
------------------

* Initial release
