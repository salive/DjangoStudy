from django.contrib.auth.models import User
from imdb.models import UserShows
from psycopg2 import DatabaseError
from imdb.utils.kinopoisk_api import KP_API


def get_user_shows_list(user_telegram_id):
    try:
        shows = UserShows.objects.select_related('show').filter(
            user__id=user_telegram_id)
    except:
        raise DatabaseError('Sometgong went wrong')

    return shows


def format_show_details(show: list):
    image = show[0]
    text = f"Название: \n {show[1]} | {show[2]}\n\n" \
           f"Год: {show[3]}\n\n" \
           f"Описание: {show[4]}\n\n"
    return image, text
