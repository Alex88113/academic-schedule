from typing import Dict

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from config_settings import *

load_dotenv()

class TestUserSettings:
    @pytest.fixture
    def initial_user_data(self) -> Dict[str, str | None]:
        return {
            'username': os.getenv('TOP_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'application_key': os.getenv('APPLICATION_KEY'),
            'id_city': None
        }

    def test_login(self, initial_user_data):
        username = {'username': initial_user_data['username']}
        obj_func = create_user_model()
        assert  obj_func['username'] == username['username']

    def test_password(self, initial_user_data):
        password_user = {
            'password': initial_user_data['password']
        }
        obj_func= create_user_model()
        assert obj_func['password'] == password_user['password']

    def test_application_key(self, initial_user_data):
        password_user = {
            'application_key': initial_user_data['application_key']
        }
        obj_func = create_user_model()
        assert obj_func['application_key'] == password_user['application_key']

    def test_id_city(self, initial_user_data):
        password_user = {
            'id_city': initial_user_data['id_city']
        }
        obj_func = create_user_model()
        assert obj_func['id_city'] == password_user['id_city']


    def test_all_user_data(self, initial_user_data):
        result = create_user_model()
        assert result == initial_user_data

