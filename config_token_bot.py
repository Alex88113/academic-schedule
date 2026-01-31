import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


load_dotenv()

class TokenTgBot(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file = '.env', env_file_encoding = 'utf-8')

token = {
    'bot_token': os.getenv('TOKEN_MY_BOT')
}
config = TokenTgBot(**token)
print(dict(config))