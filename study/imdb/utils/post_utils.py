from django.db import DatabaseError
import requests
from study import settings
from ..models import Show, UserShows, User
from django.contrib.auth.decorators import login_required


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


def add_show_to_local_database(post_request):
    '''
    Добавляет найденный на KinoPoisk фильм в локальную базу данных    
    '''
    show_id = post_request['id']
    show_title = post_request['title']
    show_poster = post_request['poster']
    show_desription = post_request['desc']
    show_year = int(post_request['year'])
    show_rating = float(post_request['rating'])

    img_data = requests.get(show_poster).content
    with open(f'{settings.BASE_DIR}\\imdb\\static\\imdb\\images\\{show_id}.jpg', 'wb') as img:
        img.write(img_data)

    try:
        new_show = Show(id=show_id,
                        title=show_title,
                        year=show_year,
                        poster=f'imdb\\static\\imdb\\images\\{show_id}.jpg',
                        rating=show_rating,
                        description=show_desription)

    except:
        raise DatabaseError('Something went wrong')

    new_show.save()
