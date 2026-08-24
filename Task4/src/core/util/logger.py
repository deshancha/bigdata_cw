# Author: Chamika Deshan
# Created: 2026-08-22

class Logger:
    def __init__(self, name: str):
        self.name = name

    def info(self, message: str):
        print(f"INFO  | [{self.name}] {message}")

    def warn(self, message: str):
        print(f"WARN  | [{self.name}] {message}")

    def error(self, message: str):
        print(f"ERROR | [{self.name}] {message}")
