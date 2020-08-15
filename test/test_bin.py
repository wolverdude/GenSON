import unittest
import json
from os import path
from subprocess import Popen, PIPE
from . import base
from genson import SchemaBuilder

BASE_SCHEMA = {"$schema": SchemaBuilder.DEFAULT_URI}
BIN_PATH = path.abspath(path.join(__file__, '..', '..', 'bin', 'genson.py'))
FIXTURE_PATH = path.abspath(path.join(__file__, '..', 'fixtures'))


def run(args=[], stdin_data=None):
    """
    Run the ``genson`` executable as a subprocess and return
    (stdout, stderr). Some assuaging is necessary to maintain
    Python compatibility with both Python 2 and 3.
    """
    genson_process = Popen([BIN_PATH] + args, stdin=PIPE, stdout=PIPE)
    if stdin_data is not None:
        stdin_data = stdin_data.encode('utf-8')
    (stdout, stderr) = genson_process.communicate(stdin_data)
    genson_process.wait()
    if isinstance(stdout, bytes):
        stdout = stdout.decode('utf-8')
    if isinstance(stderr, bytes):
        stderr = stderr.decode('utf-8')
    return (stdout, stderr)


class TestStdin(unittest.TestCase):

    def test_empty_input(self):
        (stdout, stderr) = run(stdin_data='')
        self.assertEqual(stderr, None)
        self.assertEqual(json.loads(stdout), BASE_SCHEMA)

    def test_empty_object(self):
        (stdout, stderr) = run(stdin_data='{}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"type": "object"}, **BASE_SCHEMA))

    def test_delim_newline(self):
        (stdout, stderr) = run(['-d', 'newline'], '{"hi":"there"}\n{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}}, **BASE_SCHEMA))

    def test_delim_auto_empty(self):
        (stdout, stderr) = run(['-d', ''], '{"hi":"there"}{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}}, **BASE_SCHEMA))

    def test_delim_auto_whitespace(self):
        (stdout, stderr) = run(['-d', ''], '{"hi":"there"} \n\t{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}}, **BASE_SCHEMA))

    @base.only_for_python_version('>=3.3')
    def test_encoding_unicode(self):
        (stdout, stderr) = run(['-e', 'utf-8', path.join(FIXTURE_PATH, 'utf-8.json')])
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"type": "string"}, **BASE_SCHEMA))

    @base.only_for_python_version('>=3.3')
    def test_encoding_cp1252(self):
        (stdout, stderr) = run(['-e', 'cp1252', path.join(FIXTURE_PATH, 'cp1252.json')])
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            dict({"type": "string"}, **BASE_SCHEMA))
