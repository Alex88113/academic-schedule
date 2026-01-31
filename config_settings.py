import os

from dotenv import load_dotenv
from pathlib import Path
from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    field_validator
)

from loggers_module.logger_module import *

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

class UserSettings(BaseModel):
    """
    Класс базовой валидации данных из .env
    """
    username: str
    password: str
    application_key: str
    id_city: None = None

    @field_validator('username')
    @classmethod
    def valid_login(cls, username: str):
        if isinstance(username, str) and username.strip() != '':
            return username
        else:
            raise ValueError('Возникла ошибка!\n'
            f'содержимое username: ({username})\n'
           f'тип {type(username)}')

    @field_validator('password')
    @classmethod
    def valid_password(cls, password: str):
        if isinstance(password, str) and len(password) > 1:
            return password
        else:
            raise ValueError('Проблемы с паролем\n'
            f'тип пароля: {type(password)}'
            f'содержимое password: {password}'
            )

    @field_validator('application_key')
    @classmethod
    def valid_app_key(cls, app_key: str):
        if isinstance(app_key, str) and len(app_key) > 1:
            return app_key
        else:
            raise ValueError('Возникли проблемы с токеном доступа:'
             f'app_key: {app_key}\n'
             f'Его тип: {type(app_key)}'
            )


    @field_validator('id_city')
    @classmethod
    def valid_city(cls,  id_city: None):
        if id_city is None:
            return id_city
        else:
            raise ValueError('id_city не является None\n'
             f'Текущий тип: {type(id_city)}\n'
             f'Содержимое: {id_city}'
            )

def create_user_model():
    user_data = {
        'username': os.getenv('TOP_USERNAME'),
        'password': os.getenv('PASSWORD'),
        'application_key': os.getenv('APPLICATION_KEY'),
        'id_city': None
    }
    user_model = UserSettings(**user_data).model_dump()
    return user_model
