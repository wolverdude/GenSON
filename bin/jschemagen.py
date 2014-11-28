#!/usr/bin/env python

DESCRIPTION = """
reads JSON object from stdin and outputs a basic schema for it
"""

import argparse
import json
import os
import sys
sys.path[0] = os.path.join(sys.path[0], '..')

from jschemagen import Schema


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-d', '--delimiter', metavar='DELIM',
                        help='delimiter for multiple JSON objects')
    parser.add_argument('-i', '--indent', type=int, metavar='SPACES',
                        help='indent output SPACES spaces')
    parser.add_argument('-s', '--schema',
                        help='JSON file containing starting schema')

    return parser.parse_args()


def multi_schema(s, raw, delimiter):
    lines = raw.split(delimiter)

    s = Schema()
    for line in lines:
        if line:
            s.add_object(json.loads(line))


if __name__ == '__main__':
    args = parse_args()
    raw = sys.stdin.read()

    s = Schema()

    if args.schema:
        s.add_schema(json.load(args.schema))

    if args.delimiter:
        multi_schema(s, raw, args.delimiter)
    else:
        s.add_object(json.loads(raw))

    print(s.to_json(indent=args.indent))
