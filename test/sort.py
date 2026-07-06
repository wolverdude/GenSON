def sort_lists_in_schema(schema):
    """
    Recursively traverses a schema and sorts any lists it finds.
    The sorting is stable and works on lists with mixed types.
    """
    if isinstance(schema, dict):
        for key, value in schema.items():
            schema[key] = sort_lists_in_schema(value)
        return schema
    elif isinstance(schema, list):
        new_list = [sort_lists_in_schema(item) for item in schema]
        try:
            return sorted(new_list)
        except TypeError:
            # This handles mixed types by creating a tuple of the type
            # name and the value. This ensures that types are grouped
            # together and then sorted.
            # It's safe to use str() here since only malformed custom
            # objects could cause it to fail.
            return sorted(new_list, key=lambda x: (type(x).__name__, str(x)))
    return schema
