import sys
import os

# Get the absolute path of the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)