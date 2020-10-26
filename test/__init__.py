# Mandatory file, otherwise cannot find tests.

import os
import sys

# In order to import src files into the tests
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')
