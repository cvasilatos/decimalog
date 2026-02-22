# Decima Log

A simple yet colorful Python logging library with console and JSON file output.

## Installation

```bash
pip install decimalog
```

## Usage

```python
import logging
from typing import cast
from decimalog import CustomLogger

# Set up logging (console + timestamped log file + JSONL file)
CustomLogger.setup_logging("logs", "app_log", "DEBUG")

logger: CustomLogger = cast(CustomLogger, logging.getLogger("myapp"))

logger.trace("Trace level message")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Features

- **Colorised console output** per log level (TRACE → cyan, DEBUG → blue, INFO → gray, WARNING → yellow, ERROR → red, CRITICAL → bold red)
- **TRACE** level support (`CustomLogger.TRACE = 5`)
- **Timestamped plain-text log file** written on every run
- **Append-mode JSONL log file** for structured log ingestion
