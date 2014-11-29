import unittest
import json
import os
import sys
from subprocess import Popen, PIPE

binpath = os.path.join(sys.path[0], '../bin/jschemagen.py')


def run(args=[], stdin_data=None):
    """
    Run the ``jschemagen`` executable as a subprocess and return
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

    def test_no_input(self):
        (stdout, stderr) = run()
        self.assertEqual(stderr, None)
        self.assertEqual(json.loads(stdout), {})

    def test_empty_object_stdin(self):
        (stdout, stderr) = run(['-'], '{}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"type": "object", "properties": {}})

    def test_delim_stdin(self):
        (stdout, stderr) = run(['-d', 'x', '-'], '{"hi":"there"}x{"hi":5}')
        self.assertEqual(stderr, None)
        self.assertEqual(
            json.loads(stdout),
            {"required": ["hi"], "type": "object", "properties": {
                "hi": {"type": ["integer", "string"]}}})


if __name__ == "__main__":
    unittest.main()
