# Author: Chamika Deshan
# Created: 2026-08-22

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from di.container import DiContainer

def main():
    container = DiContainer()
    
    spark = container.get_spark_session()
    logger = container.get_logger()
    usecase = container.get_usecase()
    
    dataset_path = "/opt/spark/work-dir/data/web-BerkStan.txt"
    
    # for local running, during dev only
    if not os.path.exists(dataset_path):
        dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "web-BerkStan.txt")
    
    try:
        usecase.execute(dataset_path)
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
