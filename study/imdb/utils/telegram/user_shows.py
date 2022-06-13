from django.contrib.auth.models import User
from imdb.models import UserShows, Show
from psycopg2 import DatabaseError
from imdb.utils.kinopoisk_api import KP_API


def get_user_shows_list(user_telegram_id):
    user_id = User.objects.get(username=user_telegram_id).id
    try:
        shows = UserShows.objects.select_related('show').filter(
            user__id=user_id)
    except:
        raise DatabaseError('Sometgong went wrong')

    return shows


def mark_show_as_seen(user_telegram_id, show_id, user_rating):
    user_id = User.objects.get(username=user_telegram_id).id
    shows = UserShows.objects.filter(user_id=user_id, show_id=show_id).update(
        seen=True, user_rating=user_rating)


def format_show_details(show: list):
    image = show[0]
    text = f"Название:\n {show[1]} | {show[2]}\n\n" \
           f"Год: {show[4]}\n\n" \
           f"Рейтинг: {show[3]}\n\n" \
           f"Описание: {show[5]}\n\n"
    return image, text
