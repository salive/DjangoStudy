from django.contrib import admin
from .models import Show, UserShows, Season, Episode

admin.site.register(Show)
admin.site.register(UserShows)
admin.site.register(Season)
admin.site.register(Episode)
