import asyncio

import httpx
import pytest_asyncio
import pytest
import respx

from config_settings import UserSettings, create_user_model
from schedule_parser.auth import *

class TestingAuthorization:
    @pytest.fixture
    def get_settings_user(self):
        user_schema = create_user_model()
        return {
            'username': user_schema['username'],
            'password': user_schema['password'],
            'application_key': user_schema['application_key']
        }

    @pytest.fixture
    def get_headlines_post(self):
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

    @respx.mock
    @pytest.mark.asyncio
    async def test_post_request(self, get_settings_user, get_headlines_post):
        mock_request = respx.post("https://msapi.top-academy.ru/api/v2/auth/login") \
            .respond(
            status_code=200,
            json={
                'refresh_token': 'eyJ0eXAiOiJKV1QiLCJh'
            }
        )

        async with httpx.AsyncClient() as client:
            resp = await client.post(
             'https://msapi.top-academy.ru/api/v2/auth/login',
                headers=get_headlines_post,
                json=get_settings_user)

            obj_auth = AuthorizationClient()
            result = await obj_auth.post_request()

            assert resp.status_code == 200
            assert resp.json()['refresh_token'] == 'eyJ0eXAiOiJKV1QiLCJh'
