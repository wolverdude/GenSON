#!/usr/bin/env python

"""
reads json object from stdin and outputs a basic schema for it in json
"""

import json
import os
import sys
sys.path[0] = os.path.join(sys.path[0], '..')

from jschemagen import Schema


def single_schema(raw):
    return Schema().add_object(json.loads(raw))


def multi_schema(raw):
    lines = raw.split(os.linesep)

    s = Schema()
    for line in lines:
        if line:
            s.add_object(json.loads(line))

    return s


if __name__ == '__main__':
    raw = sys.stdin.read()

    try:
        s = single_schema(raw)

    except ValueError:
        s = multi_schema(raw)

    print s.to_json(indent=4)
