import json
from typing import Dict, List, Any, Coroutine
import asyncio
from pathlib import Path
import os

import httpx
from loguru import logger
from pydantic import ValidationError

file = Path(__file__).parent.parent / "configs"
logger.debug("Производится импорт модулей в auth....")

try:
    from configs.network_configs import get_connect_settings
    from configs.headers import get_post_model
    from configs.college_api import *
    from configs.config_user_settings import create_user_model

    logger.success("Модули успешно импортированы!")

except ModuleNotFoundError as error_import:
    logger.error("Возникла ошибка при импорте модулей: {e}", e=error_import)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей")

except ImportError as error:
    logger.error("Возникла ошибка при импорте модулей: {e}", e=error)
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей: {error}")

from dotenv import load_dotenv

load_dotenv()


class Auth:
    def __init__(self) -> None:
        self.client = get_connect_settings()

        logger.debug("Проверка адреса авторизации из env....")

        if (
            not isinstance(os.getenv("AUTH_URL"), str)
            or len(os.getenv("AUTH_URL")) == 0
        ):
            raise ValueError("Данный url не является строкой или он пуст.")

        self.AUTH_URL = os.getenv("AUTH_URL")

    async def post_request(self, headers=None) -> Dict[str, Any]:
        user_data = create_user_model()
        logger.debug("Отправка пост запроса...")

        try:
            resp = await self.client.post(
                self.AUTH_URL, headers=get_post_model(), json=user_data
            )

        except httpx.HTTPStatusError as error:
            if error.response.status_code == 401:
                logger.error("Отказано в доступе {e}", e=error.response.status_code)
                raise ValueError(f"Отказано в доступе: {error}")

            elif error.response.status_code == 431:
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

        else:
            data = resp.json()
            return data
