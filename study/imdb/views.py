

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import Show, Profile
from .utils.scrapper import parse
from .utils.find_local_show import find_local


def index(request):
    if request.user.id != None:
        shows = Profile.objects.get(id=request.user.id).shows.all()
    else:
        shows = Show.objects.all()

    return render(request, 'imdb/index.html', {'shows': shows})


@login_required
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
