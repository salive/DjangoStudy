from django.db import DatabaseError
import requests
from study import settings
from ..models import Show, UserShows, User, Season, Episode
from django.contrib.auth.decorators import login_required
from .kinopoisk_api import KP_API


def add_usershow(post_request):
    '''
    Добавляет фильм в пользовательские фильмы 
    '''
    try:
        usershow = UserShows(
            user=User.objects.get(username=post_request['user']),
            show=Show.objects.get(id=post_request['film_id'])
        )

    except:
        raise DatabaseError('Something went wrong')

    usershow.save()


def add_seasons_info(show_id: str):
    '''
    Добавляет список сезонов и эпизодов для сериала
    '''
    try:
        show_object = Show.objects.get(id=show_id)
        seasons_list = KP_API.parse_response(show_id, 'seasons_info')
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


def add_show_to_local_database(post_request):
    '''
    Добавляет найденный на KinoPoisk фильм в локальную базу данных    
    '''
    show_id = post_request['id']
    show_is_series = post_request['is_series']
    show_title = post_request['title']
    show_poster = post_request['poster']
    show_desription = post_request['desc']
    show_year = int(post_request['year'])
    show_rating = float(post_request['rating'])
    img_data = requests.get(show_poster).content
    img_path = '\\imdb\\static\\imdb\\images\\'
    with open(f'{settings.BASE_DIR}{img_path}{show_id}.jpg', 'wb') as img:
        img.write(img_data)

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
