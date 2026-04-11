from loguru import logger
import sys


def create_logger_info():
    logger.add(
        'logs/result_log.log',
        colorize=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == 'INFO',
        level='INFO'
    )

def create_logger_success():
    logger.add(
    'logs/success.log',
    level='SUCCESS',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'SUCCESS',
    rotation='100 MB'
    )

def create_logger_debug():
    logger.add(
    'logs/debug.log',
    format='{time:YYY-MM-DD at HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'DEBUG',
    level='DEBUG',
    rotation='100 MB'
    )

def create_logger_warning():
    logger.add(
    'logs/warning.log',
    level='WARNING',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'WARNING',
    rotation='150 MB'
    )

def create_logger_error():
    logger.add(
    'logs/error_critical.log',
    level='ERROR',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation='200 MB'
    )
