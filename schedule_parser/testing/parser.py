import os
import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta

import httpx
from pydantic import ValidationError
from dotenv import load_dotenv
from loggers_module.logger_module import *

logger.debug("Начался импорт модулей в parser...")

try:
    from configs.college_api import ScheduleApi
    from auth import Auth
    from validation_tokens import ValidationTokens

    logger.debug("Импорт в модуле (parser) прошел успешно.")

except ModuleNotFoundError as error_import:
    logger.error(
        "Возникла ошибка при импорте модулей в (parser): {e}", e=error_import
    )
    raise

except ImportError as error:
    logger.error(
        "Возникла ошибка при импорте модулей в (parser): {e}", e=error
    )
    raise

load_dotenv()


class Parsing:
    def __init__(self, token: str) -> None:
        if (
            not isinstance(os.getenv("SCHEDULE_URL"), str)
            or len(os.getenv("SCHEDULE_URL").strip()) == 0
        ):
            raise ValueError(
                "url для получения расписания не является строкой или она пуста"
            )

        if not isinstance(token, str) or len(token.strip()) == 0:
            raise ValueError(
                "Токен должен быть строкой или не должен быть пустым"
            )

        self.token = token
        self.SCHEDULE_URL = os.getenv("SCHEDULE_URL")
        self.auth_client = Auth().client

    def get_headers_request(self, token_auth: str) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {token_auth}",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://journal.top-academy.ru",
            "Referer": "https://journal.top-academy.ru/",
            "path": "/api/v2/signal/operations/signals-list",
            "accept-encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": "Chromium;v=140, Not=A?Brand;v=24, YaBrowser;v=25.10, Yowser;v=2.5",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36",
        }
        return headers

    async def get_parsing_schedule(self) -> List[Dict[str, Any]]:
        headers = self.get_headers_request(self.token)
        client = self.auth_client
        logger.debug("Отправка гет запроса на получение расписания....")

        try:
            resp = await client.get(self.SCHEDULE_URL, headers=headers)

        except httpx.ConnectError as error:
            logger.error(
                "Не удалось установить соединение с доменом: {e}", e=error
            )
            raise
        except httpx.ConnectTimeout as error:
            logger.error("Сервер не отвечает, причина: {e}", e=error)
            raise
        except httpx.ReadTimeout as errro:
            logger.error("Сервер завис. причина: {e}", e=errro)
            raise

        else:
            data = resp.json()
            return data
