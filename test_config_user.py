import os

import httpx
import pytest
import respx

from dotenv import load_dotenv
from configs.config_user_settings import create_user_model

load_dotenv()

USERNAME = os.getenv("TOP_USERNAME")
PASSWORD = os.getenv("PASSWORD")
APPLICATION_KEY = os.getenv("APPLICATION_KEY")


@pytest.fixture
def get_settings_user():
    user_schema = create_user_model()
    return {
        "username": user_schema["username"],
        "password": user_schema["password"],
        "application_key": user_schema["application_key"],
    }


@pytest.mark.asyncio
async def test_username(get_settings_user):
    assert get_settings_user["username"] == USERNAME
    assert get_settings_user["username"] is not None
    assert len(get_settings_user["username"]) > 0


@pytest.mark.asyncio
async def test_password(get_settings_user):
    assert get_settings_user["password"] == PASSWORD
    assert get_settings_user["password"] is not None
    assert len(get_settings_user["password"]) > 0


@pytest.mark.asyncio
async def test_app_token(get_settings_user):
    assert get_settings_user["application_key"] == APPLICATION_KEY
    assert get_settings_user["application_key"] is not None
    assert len(get_settings_user["application_key"]) > 0
