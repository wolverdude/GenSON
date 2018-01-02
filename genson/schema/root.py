import json
from warnings import warn
from .node import SchemaNode


class Genson(object):
    """
    ``Genson`` is the basic schema generator class. ``Genson``
    objects can be loaded up with existing schemas and objects before
    being serialized.
    """
    DEFAULT_URI = 'http://json-schema.org/schema#'
    NULL_URI = 'NULL'

    def __init__(self, schema_uri=None):
        """
        :param schema_uri: value of the ``$schema`` keyword. If not
          given, it will use the value of the first available
          ``$schema`` keyword on an added schema or else the default:
          ``'http://json-schema.org/schema#'``
        """

        self._root_node = SchemaNode()
        self.schema_uri = schema_uri

    def add_schema(self, schema):
        """
        Merge in a JSON schema. This can be a ``dict`` or another
        ``Genson``

        :param schema: a JSON Schema

        .. note::
            There is no schema validation. If you pass in a bad schema,
            you might get back a bad schema.
        """
        if isinstance(schema, Genson):
            schema_uri = schema.schema_uri
            schema = schema.to_schema()
            if schema_uri is None:
                del schema['$schema']
        elif isinstance(schema, SchemaNode):
            schema = schema.to_schema()

        if '$schema' in schema:
            self.schema_uri = self.schema_uri or schema['$schema']
            schema = dict(schema)
            del schema['$schema']
        self._root_node.add_schema(schema)

    def add_object(self, obj):
        """
        Modify the schema to accomodate an object.

        :param obj: any object or scalar that can be serialized in JSON
        """
        self._root_node.add_object(obj)

    def to_schema(self):
        """
        Merges in an existing schema.

        :rtype: ``dict``
        """
        schema = self._base_schema()
        schema.update(self._root_node.to_schema())
        return schema

    def to_json(self, *args, **kwargs):
        """
        Generate a schema and convert it directly to serialized JSON.

        :rtype: ``str``
        """
        return json.dumps(self.to_schema(), *args, **kwargs)

    def __len__(self):
        """
        Number of ``SchemaGenerator`` s at the top level. This is used
        mostly to check for emptiness.
        """
        return len(self._root_node)

    def __eq__(self, other):
        """
        Check for equality with another Genson object.

        :param other: another Genson object. Other types are
          accepted, but will always return ``False``
        """
        if self is other:
            return True
        if not isinstance(other, Genson):
            return False

        return self._root_node == other._root_node

    def __ne__(self, other):
        return not self.__eq__(other)

    def _base_schema(self):
        if self.schema_uri == self.NULL_URI:
            return {}
        else:
            return {'$schema': self.schema_uri or self.DEFAULT_URI}


class Schema(Genson):

    def __init__(self):
        warn('genson.Schema is deprecated in v1.0, and it may be '
             'removed in future versions. Use genson.Genson instead.',
             PendingDeprecationWarning)
        super(Schema, self).__init__(schema_uri=Genson.NULL_URI)

    def to_dict(self, recurse='DEPRECATED'):
        warn('#to_dict is deprecated in v1.0, and it may be removed in '
             'future versions. Use #to_schema instead.',
             PendingDeprecationWarning)
        if recurse != 'DEPRECATED':
            warn('the `recurse` option for #to_dict does nothing in v1.0',
                 DeprecationWarning)
        return self.to_schema()
