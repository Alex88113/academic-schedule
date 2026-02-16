import asyncio
from typing import Dict
from datetime import datetime
import json
from abc import ABC, abstractmethod

import httpx
from pydantic import BaseModel, Field,  field_validator,  ValidationError

from loggers_module.logger_module import *

logger.debug('Импорт модуля с пользовательской конфигурацией')

try:
    from config_settings import UserSettings, create_user_model
    logger.debug("Импорт прошел успешно!")

except (ImportError, ModuleNotFoundError) as error:
    logger.error('Ошибка при импорте модуля с пользовательской конфигурацией')
    raise ValueError(f'Ошибка при импорте модуля с пользовательской конфигурацией: {error}')

class Tokens(BaseModel):
    access_token: str = None
    refresh_token: str = None

    field_validator('access_token')
    classmethod
    def valid_token(cls, token: str):
        if token is None: raise ValueError("Токен не может быть None")
        if len(token) == 0: raise ValueError("access_token не может быть пустым")
        else: return token

    field_validator('refresh_token')
    classmethod
    def valid_refresh_token(cls, token: str):
        if token is None: raise ValueError("Токен не может быть None")
        if len(token) == 0: raise ValueError("refresh_token не может быть пустым")
        else: return token

def create_settings_connections():
    timeout = httpx.Timeout(
        connect=10.0,
        read=30.0,
        write=10.0,
        pool=5
    )
    limits = httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10,
        keepalive_expiry=5.0
    )
    return httpx.AsyncClient(timeout=timeout, limits=limits)


class DataGetRequest:
    def get_headlines_post_request(self) -> Dict[str, str]:
        headers = {
            'accept': 'application/json, text/plain, */*',  # ожидаемый результат в формате json
            'accept-language': 'ru_RU, ru',
            'authorization': 'Bearer null',
            'content-type': 'application/json',  # говорим о том что отправляем на сервак
            'origin': 'https://journal.top-academy.ru',  # обязательно для безопастности (Cros защита)
            'referer': 'https://journal.top-academy.ru/',  # желательно
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru_RU, ru",
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "YaBrowser";v="25.10", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
        }
        return headers

class AuthClient(ABC):
    def __init__(self):
        self.session = create_settings_connections()
        self.base_url = 'https://msapi.top-academy.ru/api/v2/auth/login'
        self.user_data = create_user_model()
        self.get_headlines = DataGetRequest().get_headlines_post_request()
        self._token_auth = None
        self.schedule_url = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter="

    @abstractmethod
    async def post_request(self) -> Dict[str, str]:
        pass

    @abstractmethod
    async def validation_tokens(self) -> Tokens:
        pass

    @abstractmethod
    async def get_request(self) -> str:
        pass

class AuthorizationClient(AuthClient):
    async def post_request(self) -> str:
        session = create_settings_connections()
        headers = self.get_headlines
        logger.debug("Производится отправка post запроса...")
        try:
            response = await self.session.post(self.base_url, headers=headers, json=self.user_data)
            data = response.json()
            return data

        except httpx.HTTPStatusError as error:
            if error.statuis_code == 401:
                logger.error('Отказано в доступе {e}', e=error.status_code)
                raise ValueError(f"Отказано в доступе: {error}")

            elif error.status_code == 431:
                logger.error("Поля заголовков слишком длинные {e}", e=error)
                raise ValueError(f"Поля заголовков слишком длинные {error}")

        except json.JSONDecodeError as error:
            logger.error("Некорректный Json: {e}", e=error)
            raise ValueError(f"Некорректный Json: {error}")

        except PermissionError as error:
            logger.error("У вас нет прав доступа {e}", e=error)
            raise ValueError(f"У вас нет прав доступа {error}")

        except httpx.ConnectTimeout as error:
            logger.error("Истёк таймаут на подключение {e}", e=error)
            raise ValueError(f"Истёк таймаут на подключение {error}")

        except httpx.ReadTimeout as error:
            logger.error("Таймаут на чтение ответа {e}", e=error)
            raise ValueError(f"Таймаут на чтение ответа {error}")

        except httpx.ConnectError as error_connect:
            logger.error("Не удалось подключится: {e}", e=error_connect)
            raise ValueError(f"Не удалось подключится: {error_connect}")

    async def validation_tokens(self, token) -> Tokens:
        try:
            tokens = Tokens(**token).model_dump()
        except ValidationError as error:
            raise ValidationError("возникла ошибка при валидации токенов")

        if tokens:
            self._token_auth = tokens.get('refresh_token')
            return self._token_auth

        else:
            raise ValueError("Не удалось получить токен")


    async def get_request(self, token_auth: str) -> str:
        headers = {
            "Authorization": f"Bearer {token_auth}",
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://journal.top-academy.ru',
            'Referer': 'https://journal.top-academy.ru/',
            "path": "/api/v2/signal/operations/signals-list",
            "accept-encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": "Chromium;v=140, Not=A?Brand;v=24, YaBrowser;v=25.10, Yowser;v=2.5",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
        }
        date = datetime.today()
        formatted_date = date.strftime("%Y-%m-%d")
        schedule_url = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={formatted_date}"
        logger.info("Отправляется get request......")

        resp = await self.session.get(schedule_url, headers=headers)
        data = resp.json()
        schedule = "\nРАСПИСАНИЕ НА СЕГОДНЯ\n"
        for value in data:
            if value.get('date') == formatted_date:
                schedule += f"Занятие {value.get('subject_name')} | Преподаватель {value.get('teacher_name')}\n"
                schedule += f"Начало {value.get('started_at')} | Конец {value.get('finished_at')}\n"
                schedule += f"Аудитория {value.get('room_name')}\n"
                schedule += "-" * 60; schedule += "\n"

        return schedule

async def main2():
    try:
        obj_auth = AuthorizationClient()
        token = await obj_auth.post_request()
        valid_token = await obj_auth.validation_tokens(token)
        schedule = await obj_auth.get_request(valid_token)
        print(schedule)
        logger.info("Все прошло успешно!")

    except AttributeError as error:
        logger.error("возникла ошибка с: {e}", e=error)
        raise AttributeError(f"возникла ошибка с: {error}")

asyncio.run(main2())

