import asyncio
from typing import Dict
from datetime import datetime
import json

import httpx

from loggers_module.logger_module import *

logger.debug('Импорт модуля с пользовательской конфигурацией')

try:
    from config_settings import UserSettings, create_user_model
    logger.debug("Импорт прошел успешно!")

except (ImportError, ModuleNotFoundError) as error:
    logger.error('Ошибка при импорте модуля с пользовательской конфигурацией')
    raise ValueError(f'Ошибка при импорте модуля с пользовательской конфигурацией: {error}')

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

def get_headlines_post_request() -> Dict[str, str]:
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


class AuthorizationClient:
    def __init__(self):
        self.session = create_settings_connections()
        self.base_url = 'https://msapi.top-academy.ru/api/v2/auth/login'
        self.user_data = create_user_model()
        self._token_auth = None

    async def post_request(self) -> str:
        session = create_settings_connections()
        headers = get_headlines_post_request()
        logger.debug("Производится отправка post запроса...")
        try:
            response = await self.session.post(self.base_url, headers=headers, json=self.user_data)
            data = response.json()
            token = data.get('refresh_token')
            logger.debug('Данные получены!')
            if token:
                logger.debug("Токен доступа получен!")
                self._token_auth = token
                return self._token_auth
            else: raise ValueError("Токена авторизации нет!")

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
