#!/usr/bin/env python

DESCRIPTION = """
read one or more JSON objects from stdin and output one basic schema for them
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
                        help='JSON file containing starting schema ' +
                        '(can be specified mutliple times to merge schemas)')
    parser.add_argument('-m', '--multi', action='store_true',
                        help='take multiple JSON objects from stdin')
    parser.add_argument('-d', '--delimiter', metavar='DELIM',
                        default=os.linesep, help='set delimiter for ' +
                        'JSON objects (EOL default)')
    parser.add_argument('-a', '--no-merge-arrays', action='store_false',
                        help='don\'t assume that all elements of an array ' +
                        'share the same schema')
    parser.add_argument('object', nargs=argparse.REMAINDER, default=[],
                        help='JSON file containing base object (can pass ' +
                        'multiple object files to create a unified schema')

    return parser.parse_args()


def multi_schema(s, raw, delimiter):
    lines = raw.split(delimiter)

    s = Schema()
    for line in lines:
        if line:
            s.add_object(json.loads(line))


if __name__ == '__main__':
    args = parse_args()

    s = Schema(merge_arrays=args.no_merge_arrays)

    for schema_file in args.schema:
        with open(schema_file, 'r') as fp:
            s.add_schema(json.load(fp))

    for object_file in args.object:
        with open(object_file, 'r') as fp:
            s.add_object(json.load(fp))

    print(s.to_json(indent=args.indent))
