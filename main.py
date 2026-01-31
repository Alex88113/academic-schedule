import asyncio

try:
    from commands_bot import dp, bot
    from loggers_module.logger_module import logger
    logger.info("Все модули успешно импортированы в main.py")

except ModuleNotFoundError as error:
    logger.error("Возникла ошибка при импорте модулей из commands_bot.py")
    raise ValueError(f"Возникла ошибка при импорте модулей из commands_bot.py: {error}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Бот успешно запущен!')
    asyncio.run(main())

