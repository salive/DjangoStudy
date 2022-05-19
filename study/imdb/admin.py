from django.contrib import admin
from .models import User, Show, UserShows
admin.site.register(User)
admin.site.register(Show)
admin.site.register(UserShows)
