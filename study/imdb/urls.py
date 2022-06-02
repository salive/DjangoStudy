from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'imdb'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', views.search, name='search'),
    path('films/', views.films, name='films'),
    path('films/<int:show_id>/', views.show_detail, name='show_detail'),
] + staticfiles_urlpatterns()
