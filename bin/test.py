#!/usr/bin/env python

import unittest
import sys
import os


def main():
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.join(sys.path[0], '../test'))

    runner = unittest.TextTestRunner()
    runner.run(tests)


if __name__ == '__main__':
    main()
