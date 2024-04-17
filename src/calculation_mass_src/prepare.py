
# __add_symlink_to_helpers__

import sys
import os

sys.path.append(f"{os.getenv('cwd', '/srv/synapse')}".replace('/', os.sep))
