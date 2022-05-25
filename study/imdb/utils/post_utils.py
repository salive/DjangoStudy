from django.db import DatabaseError
import requests
from study import settings
from ..models import Show, Profile
from django.contrib.auth.decorators import login_required


def add_show_to_user_profile(post_request):
    '''
    Добавляет найденный на KinoPoisk фильм в локальную базу данных
    и в профиль пользователя
    '''
    show_id = post_request['id']
    show_title = post_request['title']
    show_poster = post_request['poster']
    show_desription = post_request['desc']
    show_year = post_request['year']
    show_rating = float(post_request['rating'])

    img_data = requests.get(show_poster).content
    with open(f'{settings.BASE_DIR}\\imdb\\static\\imdb\\images\\{show_id}.jpg', 'wb') as img:
        img.write(img_data)

    try:
        new_show = Show(id=show_id,
                        title=show_title,
                        year=int(show_year),
                        poster=f'imdb\\static\\imdb\\images\\{show_id}.jpg',
                        rating=float(show_rating),
                        description=show_desription)
        profile = Profile.objects.get(user__username=post_request['user'])

    except:
        raise DatabaseError('Something went wrong')

    new_show.save()
    profile.shows.add(new_show)
