# Author: Chamika Deshan
# Created: 2026-08-24

import os
import sys
from core.util.logger import Logger

logger = Logger("Tsk4_Extractor")

def extract_data(size: int = 5000):
    raw_file = "data/cit-Patents.txt"
    out_file = f"data/patent_data_extracted.csv"
    
    if not os.path.exists(raw_file):
        logger.error("Dataset not found")
        return

    logger.info(f"Extracting :{size} ")
    count = 0
    with open(raw_file, "r") as infile, open(out_file, "w") as outfile:
        
        for line in infile:
            # skip meta
            if line.startswith("#"):
                continue
            
            parts = line.strip().split()
            if len(parts) == 2:
                from_node, to_node = parts[0], parts[1]
                # write with ',' seperated
                outfile.write(f"{from_node},{to_node}\n")
                count += 1
                
                if count >= size:
                    break
                    
    logger.info(f"Extraction complete")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            size_param = int(sys.argv[1])
            extract_data(size_param)
        except ValueError:
            logger.error("Invalid size")
            
    
