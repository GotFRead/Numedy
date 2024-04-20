
# __add_symlink_to_helpers__

import sys
import os

def get_root_path():
    path = __file__.split('\\')[0] + "\\"
    path += '\\'.join([x for x in __file__.split('\\')[1: -3]])
    return path.replace('/', os.sep)

sys.path.append(get_root_path())


