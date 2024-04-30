


import subprocess
import sys
import os
import asyncio

from helpers.logger import create_logger

import src.server_src
import src.calculation_mass_src

logger = create_logger('main.log')



# path_to_start_needed_process
pool_exec_files = {
    "server": "/src/server_src/main.py", 
    "calculation_mass": "/src/calculation_mass_src/main.py"
}

async def main():
    logger.info(f'_____Main START!_____')
    for alias, path in pool_exec_files.items(): 
        path = os.getcwd() + path
        path = path.replace('/', os.sep)
        logger.info(f'Start exec - {path}')
        subprocess.Popen([sys.executable, path])

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())