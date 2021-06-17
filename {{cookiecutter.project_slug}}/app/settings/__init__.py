import sys

try:
    from .local import *
except ImportError:
    from .common import *

if 'test' in sys.argv:
    from .tests import *
