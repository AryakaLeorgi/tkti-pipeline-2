import re
import json

class LogParser:
    def parse(self, log_text: str):
        return {
            "raw": log_text,
            "lines": log_text.split("\n"),
            "length": len(log_text.split("\n"))
        }
