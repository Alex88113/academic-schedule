import asyncio
from typing import Dict

import httpx
from loggers_module.logger_module import *

from datetime import datetime, timedelta


from .auth import (
    create_settings_connections,
    AuthorizationClient
)

def get_headlines_request(token: str) -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
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


class TomorrowSchedule:
    def __init__(self, auth_client: AuthorizationClient):
        self.auth_client = auth_client
        self.schedule_url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter="
        self.session = create_settings_connections()

    def get_heaedlines_request(self, token: str) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {token}",
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

    async def get_tomorrow(self) -> str:
        date = datetime.today()
        delta = timedelta(days=1)
        add_date = date + delta
        formatted_date = add_date.strftime("%Y-%m-%d")
        url = f"{self.schedule_url + formatted_date}"

        token = self.auth_client.token_auth
        headers = get_headlines_request(token)

        logger.info("Отправка get запроса....")

        try:
            response = await self.session.get(url, headers=headers)
            data = response.json()
            schedule = ''
            logger.info("Расписание на завтра получено.")
            schedule += f"📅 ДАТА ЗАНЯТИЙ ЗАВТРА {formatted_date} ЧИСЛО\n"

            for data2 in data:
                if data2['date'] == formatted_date:
                    schedule += f"⏰Начало занятия: {data2['started_at']} | 🏁 Конец: {data2['finished_at']}\n"
                    schedule += f"Пара {data2['subject_name']} | Преподаватель: {data2['teacher_name']}\n"
                    schedule += f"🏫 Аудитория: {data2['room_name']}\n"
                    schedule += '\n'

            return schedule

        except httpx.ConnectTimeout as error:
            logger.error("Не удалось установить соединение {e}", e=error)
            raise ValueError(f"Не удалось установить соединение: {error}")

        except httpx.ReadTimeout as error:
            logger.error("Сервер отвечает, но данные слишком медленно идут {e}", e=error)
            raise ValueError(f"Сервер отвечает, но данные слишком медленно идут: {error}")

        except httpx.PoolTimeout as error:
            logger.error("нет свободных соединений в пуле {e}", e=error)
            raise ValueError(f"нет свободных соединений в пуле.\nПричина: {error}")