import asyncio
import os
from pathlib import Path

import pytest
import pytest_asyncio
import respx

import httpx
from httpx import Response
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('TOP_USERNAME')
PASSWORD = os.getenv('PASSWORD')
APPLICATION_KEY = os.getenv('APPLICATION_KEY')

"""
Базовое мокирование post запросов
"""


class TestPostRequest:
    @respx.mock
    @pytest.mark.asyncio
    async def test_auth(self):
        respx.post("https://msapi.top-academy.ru/api/v2/auth/login").mock(
            return_value=Response(200, json={"access_token": "test-access-token", "refresh_token": "test-token"})
        )

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                'https://msapi.top-academy.ru/api/v2/auth/login',
                     json={
                         'application_key': APPLICATION_KEY,
                         "username": USERNAME,
                         "password": PASSWORD})

            assert resp.status_code == 200
            assert resp.json()['access_token'] == 'test-access-token'
            assert resp.json()['refresh_token'] == 'test-token'
            assert resp.json() != {}
            assert resp.json() is not None


    @respx.mock
    @pytest.mark.asyncio
    async def test_error_post(self):
        respx.post("https://msapi.top-academy.ru/api/v2/auth/login").mock(
            return_value=httpx.Response(403, json={'Warning': "некорректный формат отправленных данных"})
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://msapi.top-academy.ru/api/v2/auth/login",
                json={
                    'application_key': 'wejkfnejnfjkenf',
                    'username': 'awkfnwf',
                    'password': 'jewjfiejfije'
                }
            )
            assert response.status_code == 403
            assert response.json() == {'Warning': "некорректный формат отправленных данных"}

