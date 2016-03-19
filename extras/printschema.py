import copy

def pschema(schema, indent=2):
    """
    Pretty-print a JSON schema to a string.
    """
    return('schema = ' + _ps(0, '', copy.deepcopy(schema), indent, False))
    
def _ps(level, name, var, indent, more):
    sp = indent*level*' '
    sn = sp + '"' + name + '": ' if name else sp
    sep = ',\n' if more else '\n'
    if isinstance(var, int) or isinstance(var, float) or isinstance(var, bool):
        ss = sn + str(var) + sep
    elif isinstance(var, str):
        ss = sn + '"' + var + '"' + sep
    elif isinstance(var, list):
        if all(isinstance(i, str) for i in var):
            ss = sn + '[' + ','.join(['"'+x+'"' for x in var]) + ']' + sep
        else:
            ss = sn + '[\n'
            for i,k in enumerate(var,1):
                ss += _ps(level+1, '', k, indent, i<len(var))
            ss += sp + ']' + sep
    elif isinstance(var, dict):
        if len(var) < 1:
            ss = sn + '{}' + sep
        else:
            k,v = next(iter(var.items()))
            if len(var) == 1 and not isinstance(v, dict) and not isinstance(v, list):
                ss = sn + '{"' + k + '": "' + v + '"}' + sep
            else:
                ss = sn + '{\n'
                for k in ('type', 'required', 'additionalItems', 'additionalProperties',
                            'properties', 'patternProperties'):
                    if k in var:
                        ss += _ps(level+1, k, var[k], indent, 1)
                        del var[k]
                for i,k in enumerate(sorted(var.keys()),1):
                    ss += _ps(level+1, k, var[k], indent, i<len(var))
                ss += sp + '}' + sep
    else:
        ss = sn + "???" + sep
        print('Unknown type: ' + type(var) + ': ' + name)
    return ss
