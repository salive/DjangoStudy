from django.contrib.auth.models import User
from psycopg2 import DatabaseError


def check_registered_user(user_telegram_id):
    try:
        user = User.objects.get(username=user_telegram_id)
        return True
    except:
        return False


def user_register(user_telegram_id, name=''):
    try:
        new_user = User(username=user_telegram_id, first_name=name)
        new_user.save()
    except:
        raise DatabaseError('Something went wrong')
