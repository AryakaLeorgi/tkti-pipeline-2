import re

class ErrorExtractor:
    ERROR_PATTERNS = [
        r"Exception.*",
        r"error:.*",
        r"ERROR.*",
        r"Traceback.*",
        r"failed.*",
    ]

    def extract_main_error(self, log_text: str):
        for pattern in self.ERROR_PATTERNS:
            match = re.search(pattern, log_text, re.IGNORECASE)
            if match:
                return match.group()
        return "No clear error found."
