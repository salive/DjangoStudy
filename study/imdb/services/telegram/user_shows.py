from django.contrib.auth.models import User
from imdb.models import UserShows, Show, Season, Episode
from psycopg2 import DatabaseError
from imdb.services.kinopoisk_api import KP_API
from imdb.services.kinopoisk_api import KPResponse
from imdb.telegram_bot import bot as TeleBot


def get_user_shows(user_telegram_id, filter=None):
    '''
    Return user shows from DB 
    '''
    if filter is None:
        return None
    if filter == 'unseen':
        user_id = User.objects.get(username=user_telegram_id).id
        try:
            shows = UserShows.objects.select_related('show').filter(
                user__id=user_id, seen=False).order_by('show__title')
        except:
            raise DatabaseError('Something went wrong')
    elif filter == 'my_films':
        user_id = User.objects.get(username=user_telegram_id).id
        try:
            shows = UserShows.objects.select_related('show').filter(
                user__id=user_id, show__is_series=False).order_by('show__title')
        except:
            raise DatabaseError('Something went wrong')
    elif filter == 'my_series':
        user_id = User.objects.get(username=user_telegram_id).id
        try:
            shows = UserShows.objects.select_related('show').filter(
                user__id=user_id, show__is_series=True).order_by('show__title')
        except:
            raise DatabaseError('Something went wrong')
    else:
        return None

    return shows


def mark_show_as_seen(user_id, show_id, user_rating):
    user_id = User.objects.get(username=user_id).id
    shows = UserShows.objects.filter(user_id=user_id, show_id=show_id).update(
        seen=True, user_rating=user_rating)


def check_show_is_seen(user_id, show_id):
    try:
        show = UserShows.objects.get(
            user__username=user_id, show__id=show_id)
        return show.seen
    except:
        pass


def check_show_is_series(show_id):
    try:
        show = Show.objects.get(
            id=show_id)
        return show.is_series
    except:
        pass


def get_user_rating(user_id, show_id):
    try:
        show = UserShows.objects.get(
            user__username=user_id, show__id=show_id)
        return show.user_rating
    except:
        pass


def delete_show(user_id, show_id):
    try:
        show = UserShows.objects.filter(
            user__username=user_id, show__id=show_id)
        show.delete()
    except:
        raise DatabaseError('Не удалось удалить')


def get_seasons(show_id):
    try:
        seasons = Season.objects.filter(show__id=show_id)
        return seasons
    except Exception as ex:
        print(ex)
        return None


def get_episodes(season_id):
    try:
        episodes = Episode.objects.filter(season__id=season_id).order_by('id')
        return episodes
    except Exception as ex:
        print(ex)
        return None


def get_episode_info(episode_id) -> Episode:
    try:
        episode_info = Episode.objects.get(id=episode_id)
        return episode_info
    except Exception as ex:
        print(ex)
        return None


def subscribe_on_updates(user_id, show_id, value: bool):
    try:
        show = UserShows.objects.filter(user__username=user_id, show__id=show_id).update(
            subscribed_on_updates=value)
        return True
    except Exception as ex:
        print(ex)
        return None


def is_subscribed_on_updates(user_id, show_id):
    try:
        show = UserShows.objects.get(
            user__username=user_id, show__id=show_id)
        return show.subscribed_on_updates
    except Exception as ex:
        print(ex)
        return None


def format_show_details(show: KPResponse):
    image = show.poster
    text = f"Название:\n{show.title_ru} | {show.title_en}\n\n" \
           f"Год: {show.year}\n\n" \
           f"Рейтинг: {show.rating}\n\n" \
           f"Описание: {show.description}\n\n"
    return image, text
