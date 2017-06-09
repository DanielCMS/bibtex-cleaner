import os
import sys

test_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.realpath(os.path.join(test_dir, "../src/"))
sys.path.append(src_dir)
