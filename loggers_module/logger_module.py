from loguru import logger
import sys
import asyncio

async def create_logger_info():
    logger.add(
        'logs/result_log.log',
        colorize=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        filter=lambda record: record['level'].name == 'INFO',
        level='INFO'
    )

async def create_logger_success():
    logger.add(
    'logs/success.log',
    level='SUCCESS',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'SUCCESS',
    rotation='100 MB'
    )

async def create_logger_debug():
    logger.add(
    'logs/debug.log',
    format='{time:YYY-MM-DD at HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'DEBUG',
    level='DEBUG',
    rotation='100 MB'
    )

async def create_logger_warning():
    logger.add(
    'logs/warning.log',
    level='WARNING',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'WARNING',
    rotation='150 MB'
    )

async def create_logger_error():
    logger.add(
    'logs/error_critical.log',
    level='ERROR',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation='200 MB'
    )

async def create_all_loggers():
    await create_logger_info()
    await create_logger_success()
    await create_logger_debug()
    await create_logger_warning()
    await create_logger_error()


asyncio.run(create_all_loggers())