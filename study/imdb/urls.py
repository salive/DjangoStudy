from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', views.search, name='search'),
    path('films/', views.films, name='films')
] + staticfiles_urlpatterns()
