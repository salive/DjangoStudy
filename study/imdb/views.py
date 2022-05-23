

from django.shortcuts import render

from .forms import SearchForm
from .models import Show, UserShows, User
from .utils.scrapper import parse
from .utils.find_local_show import find_local


def index(request):
    shows = UserShows.objects.filter(user=User.objects.get(name='Yan'))

    return render(request, 'imdb/index.html', {'shows': shows})


def search(request):
    context = {}
    if request.GET['find']:
        query = request.GET['find']
        local_shows = find_local(query)
        search_target = f'https://www.film.ru/search/result?text={query}&type=all'
        filmru_shows = parse(search_target)
        context = {
            "local_shows": local_shows,
            "filmru_shows": filmru_shows
        }

    return render(request, 'imdb/search.html', context)
