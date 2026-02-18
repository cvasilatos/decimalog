import json  # noqa: D100
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, TextIO, cast


class LogFormatter(logging.Formatter):
    """Log formatter that adds colors based on log levels."""

    cyan, blue, gray, yellow, red, bold_red = (
        "\x1b[36m",
        "\x1b[34m",
        "\x1b[37m",
        "\x1b[33m",
        "\x1b[31m",
        "\x1b[31;1m",
    )
    reset = "\x1b[0m"

    bold = "\033[1m"
    reset_bold = "\033[0m"

    fmt_str = f"%(asctime)s - [%(levelname)s] - {bold}%(name)s{reset_bold} - %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors based on the log level and ensure the logger name is at most 15 characters long."""
        if len(record.name) > 20:
            record.name = record.name[-20:]

        formats = {
            5: f"{self.cyan}{self.fmt_str}{self.reset}",
            logging.DEBUG: f"{self.blue}{self.fmt_str}{self.reset}",
            logging.INFO: f"{self.gray}{self.fmt_str}{self.reset}",
            logging.WARNING: f"{self.yellow}{self.fmt_str}{self.reset}",
            logging.ERROR: f"{self.red}{self.fmt_str}{self.reset}",
            logging.CRITICAL: f"{self.bold_red}{self.fmt_str}{self.reset}",
        }
        log_fmt = formats.get(record.levelno, self.fmt_str)

        return logging.Formatter(log_fmt).format(record)


class JsonFormatter(logging.Formatter):
    """Log formatter that outputs logs in JSON format, including timestamp, level, name, message, and any extra data."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string, including timestamp, level, name, message, and any extra data if provided."""
        log_record: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=datetime.now().astimezone().tzinfo).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        # If the user passed extra={} data, include it
        if hasattr(record, "extra_data"):
            log_record["extra"] = getattr(record, "extra_data", None)

        return json.dumps(log_record)


class CustomLogger(logging.Logger):
    """Custom logger that supports a TRACE level and sets up logging with both console and file handlers."""

    TRACE: ClassVar[int] = 5
    logging.addLevelName(TRACE, "TRACE")

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a message with severity 'TRACE'."""
        if self.isEnabledFor(self.TRACE):
            self._log(self.TRACE, msg, args, **kwargs)

    @staticmethod
    def setup_logging(folder: str, filename: str, level: str) -> None:
        """Set up logging with a console handler that uses the custom LogFormatter and a file handler that writes logs in JSON format using the JsonFormatter."""
        logging.setLoggerClass(CustomLogger)

        root: logging.Logger = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)

        log_dir = Path(folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        date_time: str = datetime.now(tz=datetime.now().astimezone().tzinfo).strftime("%Y%m%d-%H%M%S")
        file_handler = logging.FileHandler(log_dir / f"{filename}-{date_time}.log", mode="w")
        file_handler.setFormatter(logging.Formatter(LogFormatter.fmt_str))

        console_handler: logging.StreamHandler[TextIO] = logging.StreamHandler()
        console_handler.setFormatter(LogFormatter())

        log_path: Path = Path(folder) / f"{filename}.jsonl"
        file_h = logging.FileHandler(log_path, mode="a")
        file_h.setFormatter(JsonFormatter())

        logging.basicConfig(level=level, handlers=[console_handler, file_handler, file_h])


if __name__ == "__main__":
    CustomLogger.setup_logging("logs", "app_log", "TRACE")
    logger: CustomLogger = cast("CustomLogger", logging.getLogger("Long.MainApp.Name"))

    logger.trace("This should be CYAN!")
    logger.info("This should be GRAY!")
    logger.error("This should be RED!")
