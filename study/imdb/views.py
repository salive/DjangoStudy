

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import Show, Profile
from .utils.kinopoisk_api import KP_API
from .utils.find_local_show import find_local
from .utils.post_utils import add_show_to_user_profile


def index(request):
    if request.user.id != None:
        shows = Profile.objects.get(id=request.user.id).shows.all()
    else:
        shows = Show.objects.all()

    # print(KP_API.send_request('films/301'))

    return render(request, 'imdb/index.html', {'shows': shows})


def search(request):
    context = {}
    if request.GET['find']:
        query = request.GET['find']
        local_shows = find_local(query)
        search_target = query
        shows = KP_API.parse_response(search_target)
        context = {
            "local_shows": local_shows,
            "shows": shows
        }

    if request.POST and request.POST['action'] == 'add_show_to_user_profile':
        add_show_to_user_profile(request.POST)

    return render(request, 'imdb/search.html', context)
