import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from BT_ProA.Config import fromConfigFile
from BT_ProA.Gcn import Net
from BT_ProA.Gui import fromGui

def main(config_version):
    # 1 - terminal mode
    # 0 - gui mode
    is_config = 1

    # relevant only if is_config = 1
    gcn_mode = 0  # 0 - run exec_   ,   1 - training

    if is_config:
        fromConfigFile(gcn_mode, config_version)
    else:
        fromGui()

def test():
    print('hello')

if __name__ == "__main__":
    main(-1)
