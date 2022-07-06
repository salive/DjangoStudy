from django.urls import path, include, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'imdb'
urlpatterns = [
    path('api/', views.ShowsList.as_view(), {'filter': 'all'}),
    path('api/user/', views.UserInfo.as_view()),
    path('api/user/shows', views.UserShowsList.as_view()),
    path('api/films', views.ShowsList.as_view(), {'filter': 'films'}),
    path('api/show/<int:show_id>/', views.ShowInfo.as_view()),
    path('api/show/<int:show_id>/add', views.AddUserShow.as_view()),
    path('api/show/<int:show_id>/delete', views.DeleteUserShow.as_view()),
    path('api/series', views.ShowsList.as_view(), {'filter': 'series'}),
    path('api/auth/', include('djoser.urls')),
    path('api/search/', views.SearchView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

] + staticfiles_urlpatterns()
