# log_util.py
# Simple timestamped logger. Modernized 2024.

import time

_LOG_LINES: list[str] = []   # module-private; flushed and cleared by flush_log()


def log(message: str) -> None:
    """Append a timestamped line to the in-memory buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    _LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write all buffered log lines to path (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in _LOG_LINES:
            f.write(line + "\n")
    _LOG_LINES.clear()
