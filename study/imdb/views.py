

from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import Show, UserShows
from .utils.kinopoisk_api import KP_API
from .utils.find_local_show import find_local
from .utils.post_utils import add_show_to_local_database, add_usershow


def index(request):
    if request.user.id != None:
        shows = UserShows.objects.select_related('show').filter(
            user__id=request.user.id)

    else:
        shows = []

    return render(request, 'imdb/index.html', {'shows': shows})


def films(request):
    try:
        shows = Show.objects.all()
        context = {'shows': shows}
    except:
        context = {}
    if request.POST and request.POST['action'] == 'add_show_to_usershows':
        add_usershow(request.POST)
    return render(request, 'imdb/films.html', context)


def search(request):
    context = {}
    if request.GET and request.GET['find']:
        query = request.GET['find']
        search_target = query
        shows = KP_API.parse_response(search_target)
        context = {
            "shows": shows
        }

    if request.POST and request.POST['action'] == 'add_show_to_local_database':
        add_show_to_local_database(request.POST)

    return render(request, 'imdb/search.html', context)
