import os
import sys
from loguru import logger

from aiogram import (
    Bot, F,
    Dispatcher, types
)
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from dotenv import load_dotenv

try:
    from schedule_parser.auth import Auth, ValidationTokens
    from schedule_parser.parser import ParsingSchedule, GetValidSchedule
    from schedule_parser.tomorrow import TomorrowSchedule
    logger.info("Модули успешно импортированы!")

except ModuleNotFoundError as error:
    logger.error("Возникла ошибка при импорте модулей из schedule_parser:{e}", e=error)
    raise ValueError(f"Возникла ошибка при импорте модулей из schedule_parser:{error}")


def setup_package_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше

    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        logger.info(f"Added to sys.path: {project_root}")

setup_package_path()
load_dotenv()

logger.remove()

logger.add(sys.stderr, format='{time} | {level} | {message}', level='INFO')

bot = Bot(os.getenv('TOKEN_MY_BOT'))
dp = Dispatcher()
logger.info('БОТ СОЗДАН!')

async def get_today_schedule():
    try:
        obj_auth = Auth()
        data_post = await obj_auth.post_request()
        valid_obj = ValidationTokens(data_post)
        valid_token = await valid_obj.valid_tokens()  # получение валидованного токена
        parse_obj = ParsingSchedule(valid_token)
        schedule_parsing = await parse_obj.get_parsing_schedule()
        obj_schedule = GetValidSchedule(schedule_parsing)
        result = await obj_schedule.get_schedule()  # получение расписания на сегодня
        await obj_auth.closing_session()


        return result

    except AttributeError as error:
        logger.error("Возникла ошибка с: {e}", e=error)
        raise AttributeError(f"Возникла ошибка с: {error}")

    except Exception as error:
        logger.error("Возникла неизвестная ошибка: {e}", e=error)
        raise Exception(f"Возникла неизвестная ошибка: {error}")

async def get_tomorrow_schedule():
    try:
        obj_auth = Auth()
        data_post = await obj_auth.post_request()
        valid_obj = ValidationTokens(data_post)
        valid_token = await valid_obj.valid_tokens()# получение валидованного токена
        parse_obj = ParsingSchedule(valid_token)
        schedule_parsing = await parse_obj.get_parsing_schedule()

        obj_tomorrow = TomorrowSchedule(schedule_parsing)
        result = await obj_tomorrow.get_tomorrow() # а это на завтра
        await obj_auth.closing_session()
        return result

    except AttributeError as error:
        logger.error("Возникла ошибка с: {e}", e=error)
        raise AttributeError(f"Возникла ошибка с: {error}")

    except Exception as error:
        logger.error("Возникла неизвестная ошибка: {e}", e=error)
        raise Exception(f"Возникла неизвестная ошибка: {error}")

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("""
Приветствую вас!\nэто телеграмм бот для парсинга учебного расписания с сайта: https://journal.top-academy.ru/
Для того, чтобы получить дополнительный список команд введите команду: /help""")

@dp.message(Command('today'))
async def get_schedule_today(message: types.Message):
    schedule = await get_today_schedule()
    await message.answer(schedule)

@dp.message(Command('today_schedule'))
async def get_schedule_on_today(message: types.Message):
    kb = [
        [types.KeyboardButton(text="учебное расписание на сегодня")]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Вы хотите получить расписание на сегодня?", reply_markup=keyboard)


@dp.message(Command('tomorrow_schedule'))
async def create_message_tomorrow(message: types.Message):
    kb = [
        [types.KeyboardButton(text="расписание на завтра")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Хотите увидеть расписание на завтра?" , reply_markup=keyboard)

@dp.message(F.text.lower() == "расписание на сегодня")
async def handle_today_schedule_button(message: types.Message):
    await message.reply(await get_today_schedule())

@dp.message(F.text.lower() == "расписание на завтра")
async def tomorrow_schedule_button(message: types.Message):
    await message.reply(await get_tomorrow_schedule())

@dp.message(Command("tomorrow"))
async def get_schedule_on_tomorrow(message: types.Message):
    schedule_tomorrow = await get_tomorrow_schedule()
    await message.answer(schedule_tomorrow)

@dp.message(Command('help'))
async def get_help(message: types.Message):
    await message.answer("""
/start: выводит приветствие с юзером
/help: предоставляет список доступных команд и выводит пояснения к ним.
к примеру:
для получения расписания на текущий день нужно сделать следующее:
чтобы его получить необходимо ввести команду: /today_schedule и далее нажать на кнопку с названием (расписание на сегодня)
Если вы хотите посмотреть расписание на завтра то тогда вам нужно:
чтобы его получить необходимо ввести команду: /tomorrow_schedule и далее нажать на кнопку с названием (расписание на завтра)
/today: выводит расписание на сегодняшний день
/tomorrow: предоставляет расписание на завтра
/today_schedule: для того, чтобы воспользоваться кнопкой для показа расписания на сегодня
/tomorrow_schedule: для того, чтобы воспользоваться кнопкой для показа расписания на 
""")