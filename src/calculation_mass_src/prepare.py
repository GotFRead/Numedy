
# __add_symlink_to_helpers__

import sys
import os

def get_root_path():
    path = __file__.split(os.sep)[0] + os.sep
    path += f'{os.sep}'.join([x for x in __file__.split(os.sep)[1: -3]])
    return path

path = f"{os.getenv('cwd', get_root_path())}"

sys.path.append(path)

