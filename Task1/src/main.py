# Author: Chamika Deshan
# Created: 2026-08-12

from dotenv import load_dotenv

from di.container import AppContainer

# python3 Task1/src/main.py
def main():
    load_dotenv()
    container = AppContainer()
    logger = container.logger()

    logger.info("influx work starting...")

    usecase = container.load_data_usecase()
    
    logger.info("influx work finished")

if __name__ == "__main__":
    main()
