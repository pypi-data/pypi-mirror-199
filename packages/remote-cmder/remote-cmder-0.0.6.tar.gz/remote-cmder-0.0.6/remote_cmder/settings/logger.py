from logging import config


def init_logger():
    log_config = {
        "version": 1,
        "root": {"handlers": ["console"], "level": "DEBUG"},
        "handlers": {
            "console": {
                "formatter": "std_out",
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            }
        },
        "formatters": {
            "std_out": {
                "format": "%(asctime)s | %(levelname)s | %(module)s::%(funcName)s:%(lineno)d | (Process Details: (%(process)d, %(processName)s), Thread Details: (%(thread)d, %(threadName)s)) | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
    }
    config.dictConfig(log_config)
