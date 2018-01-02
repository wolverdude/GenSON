import argparse
import sys
import re
import json
from . import SchemaBuilder

DESCRIPTION = """
Generate one, unified JSON Schema from one or more JSON objects
and/or JSON Schemas. It's compatible with Draft 4 and above.
"""


def main():
    args = parse_args()

    if args.schema_uri:
        builder = SchemaBuilder(schema_uri=args.schema_uri)
    else:
        builder = SchemaBuilder()

    for schema_file in args.schema:
        add_json_from_file(builder, schema_file, args.delimiter, schema=True)

    for object_file in args.object:
        add_json_from_file(builder, object_file, args.delimiter)

    print(builder.to_json(indent=args.indent))


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-d', '--delimiter', metavar='DELIM',
                        help='''set a delimiter - Use this option if the
                        input files contain multiple JSON objects/schemas.
                        You can pass any string. A few cases ('newline', 'tab',
                        'space') will get converted to a whitespace
                        character. If this option is omitted, the parser
                        will try to auto-detect boundaries''')
    parser.add_argument('-i', '--indent', type=int, metavar='SPACES',
                        help='''pretty-print the output, indenting SPACES
                        spaces''')
    parser.add_argument('-s', '--schema', action='append', default=[],
                        type=argparse.FileType('r'),
                        help='''file containing a JSON Schema (can be
                        specified multiple times to merge schemas)''')
    parser.add_argument('-$', '--schema-uri', metavar='URI', dest='schema_uri',

                        help='''the value of the '$schema' keyword (defaults
                        to {default!r} or can be specified in a schema with
                        the -s option). If {null!r} is passed, the "$schema"
                        keyword will not be included in the result.'''.format(
                            default=SchemaBuilder.DEFAULT_URI,
                            null=SchemaBuilder.NULL_URI))
    parser.add_argument('object', nargs=argparse.REMAINDER,
                        type=argparse.FileType('r'), help='''files containing
                        JSON objects (defaults to stdin if no arguments
                        are passed)''')

    args = parser.parse_args()

    args.delimiter = get_delim(args.delimiter)

    # default to stdin if no objects or schemas
    if not args.object and not sys.stdin.isatty():
        args.object.append(sys.stdin)

    if not args.schema and not args.object:
        print('GenSON: noting to do - no schemas or objects given\n')

        parser.print_help()
        sys.exit(1)

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


def add_json_from_file(builder, fp, delimiter, schema=False):
    method = getattr(builder, 'add_schema' if schema else 'add_object')

    raw_text = fp.read().strip()
    fp.close()

    for json_string in get_json_strings(raw_text, delimiter):
        method(json.loads(json_string))


def get_json_strings(raw_text, delim):
    if delim is None or delim == '':
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

    # put back the stripped character
    json_strings = [string + '}' for string in strings[:-1]]

    # the last one doesn't need to be modified
    json_strings.append(strings[-1])

    return json_strings
