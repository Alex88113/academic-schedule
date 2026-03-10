import os
import asyncio
from typing import Dict, List
from datetime import datetime, timedelta

from loguru import logger
import httpx
from pydantic import ValidationError
from dotenv import load_dotenv


logger.debug("Начался импорт модулей в parser...")

try:
    from configs.config_request import *
    from network_config import get_connect_settings
    from .auth import Auth, ValidationTokens
    logger.debug("Импорт в модуле (parser) прошел успешно.")

except ModuleNotFoundError as error_import:
    logger.error("Возникла ошибка при импорте модулей в (parser): {e}", e=error_import)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей в (parser): {error_import}")

except ImportError as error:
    logger.error("Возникла ошибка при импорте модулей в (parser): {e}", e=error)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей в (parser): {error}")

load_dotenv()

class ParsingSchedule:
    def __init__(self, token: str):
        if not isinstance(os.getenv('SCHEDULE_URL'), str) or len(os.getenv('SCHEDULE_URL').strip()) == 0:
            raise ValueError("url для получения расписания не является строкой или она пуста")

        if not isinstance(token, str) or len(token.strip()) == 0:
            raise ValueError("Токен должен быть строкой или не должен быть пустым")

        self.token = token
        self.SCHEDULE_URL = os.getenv('SCHEDULE_URL')

    def get_headlines_request(self, token_auth: str) -> Dict[str, str]:
            headers = {
                "Authorization": f"Bearer {token_auth}",
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://journal.top-academy.ru',
                'Referer': 'https://journal.top-academy.ru/',
                "path": "/api/v2/signal/operations/signals-list",
                "accept-encoding": "gzip, deflate, br, zstd",
                "sec-ch-ua": "Chromium;v=140, Not=A?Brand;v=24, YaBrowser;v=25.10, Yowser;v=2.5",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Windows",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
            }
            return headers

    async def get_parsing_schedule(self):
        headers = self.get_headlines_request(self.token)
        client = get_connect_settings()
        logger.debug("Отправка гет запроса на получение расписания....")
        resp = await client.get(self.SCHEDULE_URL, headers=headers)
        data = resp.json()
        return data

class GetValidSchedule:
    def __init__(self, schedule: List[Dict[str, str | int]]):
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

    async def get_schedule(self) -> str:
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
                schedule += "*" * 70
            else:
                return "на сегодня занятий нет"

        return schedule
