#!/usr/bin/env python

DESCRIPTION = """
JSON Schema Generator - Read one or more JSON objects and/or schemas and
output one unified schema for them all.
"""

import argparse
import sys
import os
import json

sys.path[0] = os.path.join(sys.path[0], '..')
from jschemagen import Schema


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--indent', type=int, metavar='SPACES',
                        help='indent output SPACES spaces')
    parser.add_argument('-s', '--schema', action='append', default=[],
                        type=argparse.FileType('r'),
                        help='JSON file containing base schema ' +
                        '(can be specified mutliple times to merge schemas)')
    parser.add_argument('-d', '--delimiter', metavar='DELIM',
                        help='set a delimiter - use this option if the ' +
                        'input files contain multiple JSON objects/schemas')
    parser.add_argument('-a', '--no-merge-arrays', action='store_false',
                        help='create different schemas for each element of ' +
                        'an array rather than merging them into one')
    parser.add_argument('object', nargs=argparse.REMAINDER,
                        type=argparse.FileType('r'), help='JSON file ' +
                        'containing base object (pass "-" for stdin, can ' +
                        'also accept multiple object files)')

    return parser.parse_args()


def add_json_from_file(s, fp, delimiter, schema=False):
    method = getattr(s, 'add_schema' if schema else 'add_object')

    if delimiter:
        for json_string in fp.read().split(delimiter):
            if json_string:
                method(json.loads(json_string))
    else:
        method(json.load(fp))


if __name__ == '__main__':
    args = parse_args()

    s = Schema(merge_arrays=args.no_merge_arrays)

    for schema_file in args.schema:
        add_json_from_file(s, schema_file, args.delimiter, schema=True)

    for object_file in args.object:
        add_json_from_file(s, object_file, args.delimiter)

    print(s.to_json(indent=args.indent))
