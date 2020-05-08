"""Due to I was having huge troubles with tests launching from command line. I appends the project directory to the
exploring paths. If pycharm underlines the import of this file, do not worry it is ordinary behavior.
"""
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
