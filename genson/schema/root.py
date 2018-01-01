import json
from warnings import warn
from .node import SchemaNode


class SchemaRoot(object):
    """
    root schema object. It contains headers and some extra helper
    methods, but delegates the real work to SchemaNode.
    """
    DEFAULT_URI = 'http://json-schema.org/schema#'

    def __init__(self, node_class=SchemaNode, schema_uri=None):
        """
        arguments:
        * `schema_uri` (optional - `str`):
          value of the `$schema` keyword. If not given, it will use
          the value of the first available `$schema` keyword on an added
          schema or else the default: `'http://json-schema.org/schema#'`
        """
        self._root_node = node_class()
        self.schema_uri = schema_uri

    def add_schema(self, schema):
        """
        Merges in an existing schema.

        arguments:
        * `schema` (required - `dict` or `SchemaNode`):
          an existing JSON Schema to merge.
        """
        if '$schema' in schema:
            self.schema_uri = self.schema_uri or schema['$schema']
            schema = dict(schema)
            del schema['$schema']
        self._root_node.add_schema(schema)

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.

        arguments:
        * `obj` (required - `dict`):
          a JSON object to use in generating the schema.
        """
        self._root_node.add_object(obj)

    def to_schema(self):
        """
        Convert the current schema to a `dict`.
        """
        schema = self._base_schema()
        schema.update(self._root_node.to_schema())
        return schema

    def to_dict(self, recurse='DEPRECATED'):
        warn('#to_dict is deprecated in v1.0, and it may be removed in '
             'future versions. Use #to_schema instead.',
             PendingDeprecationWarning)
        if recurse != 'DEPRECATED':
            warn('the `recurse` option for #to_dict does nothing in v1.0',
                 DeprecationWarning)
        return self.to_schema()

    def to_json(self, *args, **kwargs):
        """
        Convert the current schema directly to serialized JSON.
        """
        return json.dumps(self.to_schema(), *args, **kwargs)

    def __len__(self):
        return len(self._root_node)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self._root_node == other._root_node

    def __ne__(self, other):
        return not self.__eq__(other)

    def _base_schema(self):
        return {'$schema': self.schema_uri or self.DEFAULT_URI}
