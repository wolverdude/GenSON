#!/usr/bin/env python

import sys
import os
sys.path[0] = os.path.join(sys.path[0], os.pardir)

if __name__ == '__main__':
    from genson.cli import main
    main()
