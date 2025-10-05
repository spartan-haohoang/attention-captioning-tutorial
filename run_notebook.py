#!/usr/bin/env python3
"""
Main notebook runner script.
This is a convenience script that calls the main notebook runner.
"""

import sys
import os

# Add scripts directory to path
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, scripts_dir)

# Import and run the main notebook runner
from run_notebook import main

if __name__ == '__main__':
    main()
