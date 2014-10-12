#!/usr/bin/env python

"""
reads json object from stdin and outputs a basic schema for it in json
"""

import json
import os
import sys
sys.path[0] = os.path.join(sys.path[0], '..')

from schemagen import SchemaGen


def single_schema(raw):
    return SchemaGen().add_object(json.loads(raw))


def multi_schema(raw):
    lines = raw.split(os.linesep)

    sg = SchemaGen()
    for line in lines:
        if line:
            sg.add_object(json.loads(line))

    return sg


if __name__ == '__main__':
    raw = sys.stdin.read()

    try:
        sg = single_schema(raw)

    except ValueError:
        sg = multi_schema(raw)

    print sg.dumps(indent=4)
