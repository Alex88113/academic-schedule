from typing import List, Dict, Any
from datetime import datetime

from pydantic import ValidationError
from loguru import logger

from configs.college_api import ScheduleApi
from parser import Parsing


class TodaySchedule:
    def __init__(self, schedule: List[Dict[str, str | Any]]) -> None:
        if not isinstance(schedule, List):
                raise ValueError("Требуется список со словарями с данными результата get запроса")
        self.schedule = schedule

    def __call__(self, date_tomorrow=datetime.now()) -> str:
        return date_tomorrow.strftime("%Y-%m-%d")

    def validation_schedule(self):
        for value in self.schedule:
            try:
                data = ScheduleApi(**value)
            except ValidationError as error:
                logger.error("Возникла ошибка при валидации полученного ответа: {e}", e=error)
                raise ValidationError(f"Возникла ошибка при валидации полученного ответа: {error}")

        return self.schedule

    def get_schedule_today(self) -> str:
        schedule = ''
        data = self.validation_schedule()

        for value in data:
            if value.get('date') == self.__call__():
                schedule += f"\n📅ДАТА НАЧАЛА ЗАНЯТИЙ: {value.get('date')}\n"
                schedule += (f"Занятие {value.get('subject_name')}\n"
                                f"Преподаватель: {value.get('teacher_name')}")
                schedule += f"\n⏰Начало {value.get('Started_at')}\n"
                schedule += f"🏁Конец {value.get('finished_at')}\n"
                schedule += f"🏫Аудитория {value.get('room_name')}\n"
                schedule += "-" * 70
            else:
                return "на сегодня занятий нет"

        return schedule