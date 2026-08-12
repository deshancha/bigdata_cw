# Author: Chamika Deshan
# Created: 2026-08-12

import os
import sys
from dotenv import load_dotenv

src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from di.container import AppContainer

def main():
    load_dotenv()

    arg = sys.argv[1]
    container = AppContainer()
    logger = container.logger()
    logger.info(f"influx work starting with mode: {arg}")

    if arg == "-1":
        clear_usecase = container.clear_data_usecase()
        clear_usecase.execute()
    elif arg == "0":
        csv_file_path = os.path.abspath(
            os.path.join(src_dir, "..", "Local", "fairbanks_climate_full.csv")
        )
        load_usecase = container.load_data_usecase()
        load_usecase.execute(csv_file_path=csv_file_path)

    close_usecase = container.close_connection_usecase()
    close_usecase.execute()
    
    logger.info("influx work finished")

if __name__ == "__main__":
    main()
