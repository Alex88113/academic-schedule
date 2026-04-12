from loguru import logger
import sys


logger.add(
    'logs/result_log.log',
        colorize=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == 'INFO',
        level='INFO'
    )


logger.add(
    'logs/success.log',
    level='SUCCESS',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'SUCCESS',
    rotation='100 MB'
    )

logger.add(
    'logs/debug.log',
    format='{time:YYY-MM-DD at HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'DEBUG',
    level='DEBUG',
    rotation='100 MB'
    )

logger.add(
    'logs/warning.log',
    level='WARNING',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'WARNING',
    rotation='150 MB'
    )


logger.add(
    'logs/error_critical.log',
    level='ERROR',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation='200 MB'
)
