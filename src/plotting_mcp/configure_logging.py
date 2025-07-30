import logging.config
from typing import Dict

import structlog


def configure_logging(log_level: str = "INFO") -> Dict:
    logging_level = getattr(logging, log_level.upper(), logging.INFO)
    # Full list of processors can be found at:
    # https://www.structlog.org/en/stable/api.html#module-structlog.processors
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        # Timestamp format
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=True),
        # If some value is in bytes, decode it to a Unicode str.
        structlog.processors.UnicodeDecoder(),
    ]

    # Configuration for structlog. Shared processors and prepare structlog for the `formatter`
    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Effectively freeze configuration after creating the first bound logger.
        cache_logger_on_first_use=True,
    )

    # Capture warnings and redirect them to the logging system.
    logging.captureWarnings(True)
    # Configuration for the standard library logging module.
    logging_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(
                        colors=True,
                        exception_formatter=structlog.dev.RichTracebackFormatter(),
                    ),
                ],
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "default": {
                "level": logging_level,
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": logging_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["default"],
                "level": logging_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": logging_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": logging_level,
                "propagate": False,
            },
            "uvicorn.asgi": {
                "handlers": ["default"],
                "level": logging_level,
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_dict)
    return logging_dict
