from enum import Enum


class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    error = "error"
    warning = "warning"
    critical = "critical"
