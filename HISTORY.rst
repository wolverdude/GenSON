History
=======

0.1.0 (2014-11-29)
------------------

* Initial release.


0.2.0
-----

* **Bugfix**: Options were not propagated down to subschemas.
* **Bugfix**: Empty arrays resulted in invalid schemas because it still
  included an ``items`` property.
* **Bugfix**: ``items`` was being set to a list even when
  ``merge_arrays`` was set to ``True``. This resulted in overly
  permissive schemas because ``items`` are matched optionally by
  default.
* **Improvement**: Positional Array Matching - In order to be more
  consistent with the way JSON Schema works, the alternate to
  ``merge_arrays`` is no longer never to merge list items, but instead to
  merge them based on their position in the list.
* **Improvement**: Schema Incompatibility Warning - A schema
  incompatibility used to cause a fatal error with a nondescript
  warning. The message has been improved and it has been reduced to a
  warning.

0.2.1
-----
* **Bugfix**: ``add_schema`` failed when adding list-style array schemas.
* **Bugfix**: typo in readme
