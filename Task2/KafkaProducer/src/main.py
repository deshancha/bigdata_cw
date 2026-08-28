# Author: Chamika Deshan
# Created: 2026-08-18

import os
import sys
import time
from dotenv import load_dotenv

src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from di.container import AppContainer

def main():
    dotenv_path = os.path.abspath(os.path.join(src_dir, "..", "..", ".env"))
    load_dotenv(dotenv_path=dotenv_path)

    container = AppContainer()
    logger = container.logger()
    topic = os.getenv("KAFKA_TOPIC", "traffic-telemetry")

    logger.info("Traffic telemetry producer start")

    fetch_usecase = container.fetch_telemetry_usecase()
    parse_usecase = container.parse_telemetry_usecase()
    send_usecase = container.send_telemetry_usecase()

    connect_usecase = container.connect_producer_usecase()
    connect_usecase.execute()

    fetched_records = fetch_usecase.execute()

    if not fetched_records:
        logger.warn("No data found! Exiting.")
        return

    try:
        for current_raw in fetched_records:
            # parse
            json_record = parse_usecase.execute(current_raw)

            # send
            send_usecase.execute(topic, json_record)
            logger.info(f"Sent Record: {json_record}")

            time.sleep(1)

    except Exception as e:
        logger.error(f"Err producing: {e}")
    finally:
        close_usecase = container.close_producer_usecase()
        close_usecase.execute()

    logger.info("Producer Done!")

if __name__ == "__main__":
    main()
