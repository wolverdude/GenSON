import types


JS_TYPES = {
    types.DictType: 'object',
    types.ListType: 'array',
    types.StringType: 'string',
    types.UnicodeType: 'string',
    types.IntType: 'number',
    types.FloatType: 'number',
    types.BooleanType: 'boolean',
    types.NoneType: 'null',
}


def make_schema(obj, schema=None):
    if isinstance(obj, types.DictType):
        schema = make_schema_obj(obj, schema)
    elif isinstance(obj, types.ListType):
        schema = make_schema_list(obj, schema)
    else:
        schema = make_schema_basic(obj, schema)

    return schema


def make_schema_obj(obj, schema=None):
    if not schema:
        schema = {
            'type': 'object',
            'properties': {},
            'required': obj.keys()
        }

    # make required into sets for later intersection
    schema_required = set(schema['required'])
    required = set()

    for k, v in obj.iteritems():
        schema['properties'][k] = make_schema(v, schema['properties'].get(k))
        required.add(k)

    # limit required to only those keys in both sets
    schema['required'] = sorted(list(schema_required & required))

    return schema


def make_schema_list(items, schema=None):
    if not schema:
        schema = {
            'type': 'array',
            'items': []
        }

    for item in items:
        item_schema = make_schema(item)

        # only add schema if it's not already there.
        if item_schema not in schema['items']:
            schema['items'].append(item_schema)

    return schema


def make_schema_basic(val, schema=None):
    val_type = JS_TYPES[type(val)]

    if schema:
        add_type(schema, val_type)
    else:
        schema = {
            'type': val_type
        }
    return schema


def add_type(schema, val_type):

    if isinstance(schema['type'], types.ListType):
        if val_type not in schema['type']:
            schema['type'].append(val_type)
            schema['type'].sort()

    # not a list, compare with value
    elif schema['type'] != val_type:
        # make it a list
        schema['type'] = sorted([schema['type'], val_type])
