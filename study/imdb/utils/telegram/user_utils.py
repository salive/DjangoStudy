from django.contrib.auth.models import User
from imdb.models import UserTelegramSettings
from psycopg2 import DatabaseError
from asgiref.sync import sync_to_async


def check_registered_user(user_telegram_id):
    print('check called')
    try:
        user = User.objects.get(username=str(user_telegram_id))
        print(f'User ok: {user=}')
        return True
    except Exception as ex:
        print(ex)
        return False


def get_user_setting(user_telegram_id, setting=None):
    try:
        user_settings = UserTelegramSettings.objects.select_related('user').get(
            user__username=user_telegram_id)
        return user_settings.__dict__[setting]

    except Exception as ex:
        print(ex)


def get_username_by_telegram_id(user_telegram_id):
    user = User.objects.get(username=user_telegram_id)
    return user.first_name


def user_register(user_telegram_id, name=''):
    try:
        new_user = User(username=user_telegram_id, first_name=name)
        new_user.save()
        user_settings = UserTelegramSettings(user_id=new_user.id)
        user_settings.save()
    except Exception as ex:
        print(ex)
