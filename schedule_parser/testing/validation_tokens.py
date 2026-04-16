from typing import Dict, Any
from pathlib import Path
import asyncio

from pydantic import ValidationError
from loguru import logger

file = Path(__file__)

logger.info("Started import modules in the {m}", m=file)

try:
    from auth import Auth
    from configs.college_api import Tokens

except ModuleNotFoundError as error:
    logger.error("Возникла ошибка при импорте модулей в: {m}", m=file)
    raise

except ImportError as error:
    logger.error("Возникла ошибка при импорте модулей в: {m}", m=file)
    raise

class ValidationTokens:
    def __init__(self, token_auth: Dict[str, str | Any]) -> None:
        if not isinstance(token_auth, dict):
            raise ValueError("Данные пост запроса должны быть в формате: json")
        self._token_auth = token_auth

    logger.debug("Производится валидация токенов....")
    def valid_tokens(self) -> str:
        valid_tokens = Tokens(**self._token_auth).model_dump()

        if valid_tokens:
            self._token_auth = valid_tokens.get('refresh_token')
            return self._token_auth

        else:
            logger.error("Не удалось пройти валидацию")
            raise ValidationError("Не удалось пройти валидацию")

    logger.debug("Валидация завершена!")
