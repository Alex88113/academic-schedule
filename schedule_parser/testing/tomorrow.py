import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
import httpx
from pydantic import ValidationError


from loggers_module.logger_module import *


load_dotenv()

logger.debug("Производится импорт модулей в tomorrow")
try:
    from auth import Auth
    from configs.college_api import ScheduleApi
    from validation_tokens import ValidationTokens
    logger.debug("Импорт завершен успешно")

except ModuleNotFoundError as error:
    logger.error("Возникла ошибка при импорте модуля auth: {e}", e=error)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модуля auth: {error}")

except Exception as error:
    logger.error("Неизвестная ошибка при импорте: {e}", e=error)

class TomorrowSchedule:
    def __init__(self, schedule: List[Dict[str, str | Any]]) -> None:
        if not isinstance(os.getenv('SCHEDULE_URL'), str) or len(os.getenv('SCHEDULE_URL').strip()) == 0:
            raise ValueError("url для получения расписания не является строкой или она пуста")

        if not isinstance(schedule, List):
            raise ValueError("Требуется список со словарями с данными результата get запроса")

        self.schedule = schedule
        self.SCHEDULE_URL = os.getenv('SCHEDULE_URL')

    def __call__(self, date=datetime.now()) -> str:
        delta = timedelta(days=1)
        add_date = date + delta
        return add_date.strftime("%Y-%m-%d")

    def get_tomorrow_schedule(self) -> str:
        schedule = '📅Расписание на завтра\n'
        for value in self.schedule:
            try:
                valid_data = ScheduleApi(**value)
            except ValidationError as error:
                logger.error("Возникла ошибка при валидации полученного ответа: {e}", e=error)
                raise ValidationError(f"Возникла ошибка при валидации полученного ответа: {error}")

            if value.get('date') == self.__call__():
                schedule += f"\nПара {value.get('subject_name')}\n"
                schedule += f"Преподаватель {value.get("teacher_name")}\n"
                schedule += f"⏰Начало {value.get("started_at")}\n"
                schedule += f"🏁Конец {value.get("finished_at")}\n"
                schedule += f'🏫Аудитория {value.get("room_name")}\n'
                schedule +=  "-" * 30

        return schedule