

from django.shortcuts import render
from .models import Show


def index(request):
    shows = Show.objects.all()
    return render(request, 'imdb/index.html', {'shows': shows})
