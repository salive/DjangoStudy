import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from django.conf import settings
from imdb.utils.telegram.user_utils import check_registered_user, user_register, get_username_by_telegram_id
from imdb.utils.telegram.user_shows import get_user_shows_list, format_show_details


bot = Bot(token=settings.TELEGRAM_API_KEY)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not check_registered_user(message.from_user.id):
        print(message.from_user.id)
        await message.answer("Привет, похоже мы еще не знакомы! Как тебя зовут?")
    else:
        await message.answer(message.from_user.id,
                             f"Привет, {get_username_by_telegram_id(message.from_user)}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
