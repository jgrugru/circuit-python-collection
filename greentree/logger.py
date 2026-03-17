class Logger:
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"

    COLORS = {
        "INFO": "\033[92m",  # Green
        "DEBUG": "\033[94m",  # Blue
        "WARN": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
    }

    def _log(self, level: str, text: str) -> None:
        color = self.COLORS.get(level, self.RESET)
        print(f"{self.BOLD}{color}[{level}]{self.RESET} {text}")

    def info(self, text: str) -> None:
        self._log("INFO", text)

    def debug(self, text: str) -> None:
        self._log("DEBUG", text)

    def warn(self, text: str) -> None:
        self._log("WARN", text)

    def error(self, text: str) -> None:
        self._log("ERROR", text)
