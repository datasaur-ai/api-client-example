# https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging
import json
import logging


class StructuredMessage:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def __str__(self) -> str:
        return json.dumps(self.kwargs)


def log(message, logger: logging.Logger, level=logging.INFO, **kwargs):
    logger.log(
        level=level,
        msg=StructuredMessage(
            **kwargs,
            logger=logger.name,
            level=logging._levelToName[level],
            message=message
        ),
    )
