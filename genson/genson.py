DESCRIPTION = """
generate one, unified JSON Schema from one or more
JSON objects and/or JSON Schemas.
(uses Draft 4 - http://json-schema.org/draft-04/schema)
"""

import argparse
import json
import sys
from .generator import Schema


def main():
    args = parse_args()

    s = Schema(merge_arrays=args.no_merge_arrays)

    for schema_file in args.schema:
        add_json_from_file(s, schema_file, args.delimiter, schema=True)

    for object_file in args.object:
        add_json_from_file(s, object_file, args.delimiter)

    print(s.to_json(indent=args.indent))


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-a', '--no-merge-arrays', action='store_false',
                        help='''generate a different subschema for each element
                        in an array rather than merging them all into one''')
    parser.add_argument('-d', '--delimiter', metavar='DELIM',
                        help='''set a delimiter - use this option if the
                        input files contain multiple JSON objects/schemas''')
    parser.add_argument('-i', '--indent', type=int, metavar='SPACES',
                        help='''indent output SPACES spaces''')
    parser.add_argument('-s', '--schema', action='append', default=[],
                        type=argparse.FileType('r'),
                        help='''JSON file containing a base schema (can be
                        specified mutliple times to merge schemas)''')
    parser.add_argument('object', nargs=argparse.REMAINDER,
                        type=argparse.FileType('r'), help='''files containing
                        JSON objects (defaults to stdin if no arguments
                        are passed and the -s option is not present)''')

    args = parser.parse_args()

    # default to stdin if no objects or schemas
    if not args.object and not args.schema:
        args.object.append(get_stdin())

    return args


def get_stdin():
    """
    Grab stdin, printing simple instructions if it's interactive.
    """
    if sys.stdin.isatty():
        print('Enter a JSON object, then press ctrl-D')
    return sys.stdin


def add_json_from_file(s, fp, delimiter, schema=False):
    method = getattr(s, 'add_schema' if schema else 'add_object')

    raw_text = fp.read().strip()
    fp.close()

    if not raw_text:
        pass
    elif delimiter:
        for json_string in raw_text.split(delimiter):
            if json_string:
                method(json.loads(json_string))
    else:
        method(json.loads(raw_text))
