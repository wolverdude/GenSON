import unittest
import json
from subprocess import Popen, PIPE

binpath = 'bin/genson.py'


def run(args=[], stdin_data=None):
    """
    Run the ``genson`` executable as a subprocess and return
    (stdout, stderr). Some assuaging is necessary to maintain
    Python compatibility with both Python 2 and 3.
    """
    bin = Popen([binpath] + args, stdin=PIPE, stdout=PIPE)
    if stdin_data is not None:
        stdin_data = stdin_data.encode('utf-8')
    (stdout, stderr) = bin.communicate(stdin_data)
    bin.wait()
    if isinstance(stdout, bytes):
        stdout = stdout.decode('utf-8')
    if isinstance(stderr, bytes):
        stderr = stderr.decode('utf-8')
    return (stdout, stderr)


class TestStdin(unittest.TestCase):

    def test_empty_input(self):
        (stdout, stderr) = run(stdin_data='')
        self.assertEqual(stderr, None)
        self.assertEqual(json.loads(stdout), {})

    def test_empty_object(self):
        (stdout, stderr) = run(stdin_data='{}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"type": "object", "properties": {}})

    def test_delim_newline(self):
        (stdout, stderr) = run(['-d', 'newline'], '{"hi":"there"}\n{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}})

    def test_delim_auto_empty(self):
        (stdout, stderr) = run(['-d', ''], '{"hi":"there"}{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}})

    def test_delim_auto_whitespace(self):
        (stdout, stderr) = run(['-d', ''], '{"hi":"there"} \n\t{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}})
