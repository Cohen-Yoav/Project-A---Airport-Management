import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from BT_ProA import Main as mbt

"""
This test check if we can activate the Offline planner
Offline planner is a module design by Bar and Tom
"""

if __name__ == "__main__":  
    mbt.main(0.1)