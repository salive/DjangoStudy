

from django.shortcuts import render

from .forms import SearchForm
from .models import Show
from .utils.scrapper import parse


def index(request):
    shows = Show.objects.all()
    return render(request, 'imdb/index.html', {'shows': shows})


def search(request):
    form = SearchForm()
    context = {
        "form": form
    }
    if request.method == 'POST':
        query = request.POST['search']
        search_target = f'https://www.film.ru/search/result?text={query}&type=all'
        movies = parse(search_target)
        context = {
            "form": form,
            "movies": movies
        }
        print(movies)
        return render(request, 'imdb/search.html', context)

    return render(request, 'imdb/search.html', context)
