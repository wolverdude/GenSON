import argparse
import sys
import re
import json
from .generator import Schema

DESCRIPTION = """
Generate one, unified JSON Schema from one or more
JSON objects and/or JSON Schemas.
(uses Draft 4 - http://json-schema.org/draft-04/schema)
"""


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
                        help='''set a delimiter - Use this option if the
                        input files contain multiple JSON objects/schemas.
                        You can pass any string. A few cases ('newline', 'tab',
                        'space') will get converted to a whitespace character,
                        and if empty string ('') is passed, the parser will
                        try to auto-detect where the boundary is.''')
    parser.add_argument('-i', '--indent', type=int, metavar='SPACES',
                        help='''pretty-print the output, indenting SPACES
                        spaces''')
    parser.add_argument('-s', '--schema', action='append', default=[],
                        type=argparse.FileType('r'),
                        help='''file containing a JSON Schema (can be
                        specified multiple times to merge schemas)''')
    parser.add_argument('object', nargs=argparse.REMAINDER,
                        type=argparse.FileType('r'), help='''files containing
                        JSON objects (defaults to stdin if no arguments
                        are passed and the -s option is not present)''')

    args = parser.parse_args()

    args.delimiter = get_delim(args.delimiter)

    # default to stdin if no objects or schemas
    if not args.object and not args.schema:
        args.object.append(get_stdin())

    return args


def get_delim(delim):
    """
    manage special conversions for difficult bash characters
    """
    if delim == 'newline':
        delim = '\n'
    elif delim == 'tab':
        delim = '\t'
    elif delim == 'space':
        delim = ' '

    return delim


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

    for json_string in get_json_strings(raw_text, delimiter):
        method(json.loads(json_string))


def get_json_strings(raw_text, delim):
    if delim is None:
        json_strings = [raw_text]
    elif delim == '':
        json_strings = detect_json_strings(raw_text)
    else:
        json_strings = raw_text.split(delim)

    # sanitize data before returning
    return [string.strip() for string in json_strings if string.strip()]


def detect_json_strings(raw_text):
    """
    Use regex with lookaround to spot the boundaries between JSON objects.
    Unfortunately, it has to match *something*, so at least one character
    must be removed and replaced.
    """
    strings = re.split('}\s*(?={)', raw_text)

    json_strings = []
    for string in strings:
        # put back the stripped character
        json_strings.append(string + '}')

    # the last one doesn't need to be modified
    json_strings[-1] = strings[-1]

    return json_strings
