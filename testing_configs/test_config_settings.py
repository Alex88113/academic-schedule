import pytest
from pathlib import Path
import sys



sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def user_settings_class():
    from config_user_settings import UserSettings
    return UserSettings

@pytest.fixture
def valid_user_data():
    return {
        "username": "test_user",
        "password": '34343434',
        "application_key": "test_token",
        'id_city': 3
    }

@pytest.fixture
def invalid_user_data_empty_username():
    return {
        "username": "",
        "password": '34343434',
        "application_key": "test_token",
        'id_city': None
    }

@pytest.fixture
def invalid_user_data_short_password():
    return {
        "username": "test_user",
        "password": '3',
        "application_key": "test_token",
        'id_city': 3
    }

@pytest.fixture
def invalid_user_data_empty_app_key():
    return {
        "username": "test_user",
        "password": '34343434',
        "application_key": "",
        'id_city': 3
    }

