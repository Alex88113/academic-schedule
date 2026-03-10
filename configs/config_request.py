from typing import Dict
from datetime import datetime
from datetime import date

from pydantic import BaseModel, field_validator

class ScheduleApi(BaseModel):
    date: str =  None
    lesson: int =  None
    started_at: str =  None
    finished_at: str =  None
    teacher_name: str =  None
    subject_name: str =  None
    room_name: str =  None

class Tokens(BaseModel):
    access_token: str = None
    refresh_token: str = None

class HeadlinesPost:
    def create_model_post(self) -> Dict[str, str]:
        headers = {
            'accept': 'application/json, text/plain, */*',  # ожидаемый результат в формате json
            'accept-language': 'ru_RU, ru',
            'authorization': 'Bearer null',
            'content_type': 'application/json',  # говорим о том что отправляем на сервак
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
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
        }
        return headers


def get_post_model():
    obj_post = HeadlinesPost()
    result = obj_post.create_model_post()
    return result

