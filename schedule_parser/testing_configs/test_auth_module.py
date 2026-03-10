import asyncio

from loguru import logger
import httpx
import pytest_asyncio
import pytest
import respx

logger.debug("Производится импорт модулей в модуль с тестирование авторизации")

try:
    from configs.config_user_settings import UserSettings, create_user_model
    from auth import Auth, ValidationTokens
    logger.success("Импорт прошел успешно!")

except ModuleNotFoundError as error_import:
    raise ModuleNotFoundError(f"Возникла ошибка при импорте модулей: {error_import}")

except ImportError as error_import:
    raise ImportError(f"Возникла ошибка при импорте модулей: {error_import}")


async def test_post_request(httpx_mock):
    httpx_mock.add_response(
        url="https://msapi.top-academy.ru/api/v2/auth/login",
        status_code=200)
    authorization = Auth()
    post_data = await authorization.post_request()
    assert post_data is not None
