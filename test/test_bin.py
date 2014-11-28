import unittest
import json
import os
import sys
from subprocess import Popen, PIPE

binpath = os.path.join(sys.path[0], '../bin/jschemagen.py')


def run(args=[], stdin_data=None):
    bin = Popen([binpath] + args, stdin=PIPE, stdout=PIPE)
    (stdout, stderr) = bin.communicate(stdin_data)
    bin.wait()
    return (stdout, stderr)


class TestBin(unittest.TestCase):

    def test_no_input(self):
        (stdout, stderr) = run()
        self.assertEqual(stderr, None)
        self.assertEqual(stdout.rstrip(os.linesep), '{}')

    def test_empty_object_stdin(self):
        (stdout, stderr) = run(['-'], '{}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            stdout.rstrip(os.linesep),
            json.dumps({"type": "object", "properties": {}}))

    def test_delim_stdin(self):
        (stdout, stderr) = run(['-d', 'x', '-'], '{"hi":"there"}x{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            stdout.rstrip(os.linesep),
            json.dumps({"required": ["hi"], "type": "object",
                       "properties": {"hi": {"type": ["number", "string"]}}}))
