import json
import os
from typing import Dict, List
import asyncio
from datetime import datetime

import httpx
from loguru import logger
from pydantic import ValidationError

logger.debug("Производится импорт модулей....")

try:
    from configs.config_request import *
    from configs.config_user_settings import UserSettings, create_user_model

    logger.success("Модули успешно импортированы!")

except ModuleNotFoundError as error_import:
    logger.error("Возникла ошибка при импорте модулей: {e}", e=error_import)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей")

except ImportError as error:
    logger.error("Возникла ошибка при импорте модулей: {e}", e=error)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей: {error}")

from dotenv import load_dotenv
load_dotenv()

AUTH_URL = os.getenv('AUTH_URL')
SCHEDULE_URL = os.getenv('SCHEDULE_URL')

class Auth:
    def __init__(self, timeout: float = 20.0):
        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers={"Accept": "application/json"}
        )
        logger.debug("Проверка адресов из env....")
        if not isinstance(os.getenv('AUTH_URL'), str) or len(os.getenv('AUTH_URL')) == 0:
            raise ValueError("Данный url не является строкой или он пуст.")

        if not isinstance(os.getenv('SCHEDULE_URL'), str) or len(os.getenv('AUTH_URL')) == 0:
            raise ValueError("url для получения расписания не является строкой или он пуст.")
        logger.debug("Проверка завершена.\nАдреса получены!")

    async def aclose(self) -> None:
        await self._client.aclose()

    async def post_request(self) -> Dict[str, str]:
        user_data = create_user_model()
        logger.debug("Отправка пост запроса...")
        try:
            resp = await self._client.post(AUTH_URL,
            headers=get_post_model(), json=user_data)
            data = resp.json()
            return data

        except httpx.HTTPStatusError as error:
            if error.status_code == 401:
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

class ValidationTokens:
    def __init__(self, token_auth: Dict[str, str]):
        if not isinstance(token_auth, dict):
            raise ValueError("Данные пост запроса должны быть в формате: json")
        self._token_auth = token_auth

    logger.debug("Производится валидация токенов....")
    async def valid_tokens(self) -> str:
        valid_tokens = Tokens(**self._token_auth).model_dump()

        if valid_tokens:
            self._token_auth = valid_tokens.get('refresh_token')
            return self._token_auth

        else:
            logger.error("Не удалось пройти валидацию")
            raise ValidationError("Не удалось пройти валидацию")

    logger.debug("Валидация завершена!")

async def get_valid_token():
    auth = Auth()
    data_post = await auth.post_request()
    valid_obj = ValidationTokens(data_post)
    token = await valid_obj.valid_tokens()
    return token
