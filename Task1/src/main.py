# Author: Chamika Deshan
# Created: 2026-08-12

from dotenv import load_dotenv
from di.container import AppContainer

# python3 Task1/src/main.py
def main():
    load_dotenv()
    container = AppContainer()
    logger = container.logger()

    logger.info("Application starting...")

if __name__ == "__main__":
    main()
