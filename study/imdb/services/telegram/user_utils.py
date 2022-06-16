from genericpath import exists
from django.contrib.auth.models import User
from imdb.models import UserTelegramSettings
from psycopg2 import DatabaseError
from imdb.telegram_bot import bot as TeleBot
from imdb.services.telegram.markups import find_results_markup


def check_registered_user(user_telegram_id):
    '''
    Check if user with Telegram ID passed, registered in local DB
    '''
    try:
        is_registered = User.objects.filter(
            username=str(user_telegram_id)).exists()

    except Exception as ex:
        raise ex

    return is_registered


def user_register(message):
    '''
    Register user in local DB
    '''
    name = message.text
    try:
        new_user = User(username=message.from_user.id, first_name=name)
        new_user.save()
        user_settings = UserTelegramSettings(user_id=new_user.id)
        user_settings.save()
        TeleBot.bot.authenticated_users[message.from_user.id] = True
        TeleBot.bot.send_message(message.from_user.id,
                                 "Добро пожаловать!", reply_markup=TeleBot.default_markup())
        return True
    except Exception as ex:
        raise ex


def get_user_setting(user_telegram_id, setting=None):
    '''
    Retrieve user settings
    '''

    try:
        user_settings = UserTelegramSettings.objects.select_related('user').get(
            user__username=user_telegram_id)
        return user_settings.__dict__[setting]

    except Exception as ex:
        raise ex


def get_username_by_telegram_id(user_telegram_id):
    user = User.objects.get(username=user_telegram_id)
    return user.first_name


def find_show(message):
    target = message.text
    if target in TeleBot.bot.Commands._value2member_map_:
        TeleBot.bot.send_message(message.from_user.id,
                                 'Кажется, ты ввел команду')
        return
    TeleBot.bot.send_message(message.from_user.id,
                             'Вот, что я нашел:', reply_markup=find_results_markup(message))
