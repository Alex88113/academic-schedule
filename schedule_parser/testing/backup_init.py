import asyncio
from pathlib import Path

from loggers_module.logger_module import *

file = Path(__file__)

logger.debug("Started import modules in the {f}", f=file)
try:
    from auth import Auth
    from validation_tokens import ValidationTokens
    from today import TodaySchedule
    from parser import Parsing
    from tomorrow import TomorrowSchedule

    logger.debug("import is success!")

except ModuleNotFoundError as error:
    logger.error(
        "Возникла ошибка при импорте модулей в {f}: {e}", f=file, e=error
    )
    raise

except ImportError as error:
    logger.error(
        "Возникла ошибка при импорте модулей в {f}: {e}", f=file, e=error
    )
    raise


async def main():
    try:
        auth_client = Auth()
        post_data = await auth_client.post_request()
        obj_valid = ValidationTokens(post_data)
        valid_token = obj_valid.valid_tokens()

        obj_parsing = Parsing(valid_token)
        parsing_data = await obj_parsing.get_parsing_schedule()
        obj_today = TodaySchedule(parsing_data)
        today_schedule = obj_today.get_schedule_today()

        obj_tomorrow = TomorrowSchedule(parsing_data)
        tomorrow_schedule = obj_tomorrow.get_tomorrow_schedule()

        logger.info(tomorrow_schedule)
        print(tomorrow_schedule)

    except ValueError as error:
        logger.error("Некорректно переданные аргументы: {e}", e=error)
        raise

    except Exception as error:
        logger.error("Возникла непредвиденная ошибка: {e}", e=error)
        raise


if __name__ == "__main__":
    asyncio.run(main())
