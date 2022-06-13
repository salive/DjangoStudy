from django.db import DatabaseError
import requests
from study import settings
from ..models import Show, UserShows, User, Season, Episode
from django.contrib.auth.decorators import login_required
from .kinopoisk_api import KP_API


def check_usershow_exists(user_telegram_id, show_id):
    user_id = User.objects.get(username=user_telegram_id).id
    if UserShows.objects.filter(user_id=user_id, show_id=show_id).exists():
        return True
    return False


def add_usershow(user_id, show_id):
    '''
    Добавляет фильм в пользовательские фильмы 
    Возвращает True при успешном добавлении, False если шоу уже в списке пользователя
    '''
    add_show_to_local_database(show_id)
    if not check_usershow_exists(user_id, show_id):
        usershow = UserShows(
            user=User.objects.get(username=user_id),
            show=Show.objects.get(id=show_id))
        usershow.save()
        return True
    return False


def add_seasons_info(kinopoisk_id: str):
    '''
    Добавляет список сезонов и эпизодов для сериала
    '''
    try:
        show_object = Show.objects.get(id=kinopoisk_id)
        seasons_list = KP_API.parse_response(kinopoisk_id, 'seasons_info')
        for s in seasons_list:
            season = Season(show=show_object,
                            season_number=s[0][0],
                            num_episodes=len(s),
                            air_date=s[0][-1]
                            )
            season.save()
            for ep in s:
                episode = Episode(season=season,
                                  episode_number=ep[1],
                                  titleRu=ep[2],
                                  titleEn=ep[3],
                                  description=ep[4],
                                  air_date=ep[5])
                episode.save()
    except:
        raise DatabaseError('Something went wrong')
    pass


def add_show_to_local_database(kinopoisk_id):
    '''
    Добавляет найденный на KinoPoisk фильм в локальную базу данных   

    '''
    if Show.objects.filter(id=kinopoisk_id).exists():
        return False

    show_details = KP_API.parse_response(kinopoisk_id, 'show_details')

    show_id = kinopoisk_id
    show_poster = show_details[0]
    img_data = requests.get(show_poster).content
    img_path = '\\imdb\\static\\imdb\\images\\'
    with open(f'{settings.BASE_DIR}{img_path}{show_id}.jpg', 'wb') as img:
        img.write(img_data)
    show_title = show_details[1]
    show_rating = show_details[3]
    show_year = int(show_details[4])
    show_desription = show_details[5]
    if show_details[6] in ['TV_SERIES',  'MINI_SERIES']:
        show_is_series = True
    else:
        show_is_series = False

    try:
        new_show = Show(id=show_id,
                        title=show_title,
                        year=show_year,
                        poster=f'{img_path}{show_id}.jpg',
                        rating=show_rating,
                        description=show_desription,
                        is_series=show_is_series)

    except:
        raise DatabaseError('Something went wrong')

    new_show.save()
    if show_is_series:
        add_seasons_info(kinopoisk_id)
