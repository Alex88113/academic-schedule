import asyncio

from loggers_module.logger_module import *

try:
    logger.debug("Производится импорт модулей")
    from .auth import AuthorizationClient
    from .parser import ScheduleParser
    logger.debug("Импорт модулей произведен успешно!")

except (ModuleNotFoundError, ImportError) as error_import:
    logger.error("Ошибка при импорте модулей: {e}", e=error_import)
    raise ValueError(f'Ошибка при импорте модулей: {error_import}')

async def get_schedule_parser():
    obj_auth = AuthorizationClient()
    obj_schedule = ScheduleParser(obj_auth)
    result = await obj_auth.post_request()
    schedule = await obj_schedule.get_request()
    return schedule