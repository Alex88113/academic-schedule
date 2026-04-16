import asyncio

import pytest
import respx
import httpx

from auth import Auth

class TestAuthService:
    @respx.mock
    @pytest.mark.asyncio
    async def test_mock_authorization(self):
        respx.post('https://msapi.top-academy.ru/api/v2/auth/login').mock(
            return_value=httpx.Response(200, json={'refresh_token': 'test-refresh_token', 'access_token': 'test-access'})
        )

        auth_client = Auth()
        assert await auth_client.post_request() == {'refresh_token': 'test-refresh_token', 'access_token': 'test-access'}
        assert await auth_client.post_request() is not None
        assert await auth_client.post_request() != {}

    @pytest.mark.asyncio
    async def test_auth(self):
        auth_client = Auth()
        result = await auth_client.post_request()

        assert 'refresh_token' in result
        assert result != {}
        assert result['refresh_token'] != ""
        assert result['expires_in_refresh'] > 0

        assert 'access_token' in result
        assert result['access_token'] != ''
        assert result['expires_in_access'] > 0
