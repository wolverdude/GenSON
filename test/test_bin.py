import unittest
import json
import os
import sys
from subprocess import Popen, PIPE

binpath = os.path.join(sys.path[0], '../bin/jschemagen.py')


def run(stdin_data=None):
    bin = Popen([binpath], stdin=PIPE, stdout=PIPE)
    (stdout, stderr) = bin.communicate(stdin_data)
    bin.wait()
    return (stdout, stderr)


class TestBin(unittest.TestCase):

    def test_no_input(self):
        (stdout, stderr) = run()
        self.assertEqual(stderr, None)
        self.assertEqual(stdout.rstrip(os.linesep), '{}')

    def test_empty_object(self):
        (stdout, stderr) = run('{}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            stdout.rstrip(os.linesep),
            json.dumps({"type": "object", "properties": {}}, indent=4))
