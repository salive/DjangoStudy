from .serializers import ShowSerializer, UserSerializer, UserShowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Show, UserShows
from django.contrib.auth.models import User
from .services.shows_add_utils import add_usershow_from_web


class ShowsList(APIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        shows = []
        match self.kwargs['filter']:
            case 'films':
                shows = Show.objects.filter(is_series=False).order_by('title')
            case 'series':
                shows = Show.objects.filter(is_series=True).order_by('title')
            case 'all':
                shows = Show.objects.all().order_by('title')
        return shows

    def get(self, request, *args, **kwargs):
        shows = self.get_queryset()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)

    permission_classes = ()


class UserInfo(APIView):

    def get_queryset(self, id):
        user_info = User.objects.filter(id=id)
        return user_info

    def get(self, request, *args, **kwargs):
        user_info = self.get_queryset(request.user.id)
        serializer = UserSerializer(user_info, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class UserShowsList(APIView):

    def get_queryset(self, id):
        user_shows = UserShows.objects.filter(user_id=id)
        return user_shows

    def get(self, request, *args, **kwargs):
        user_shows = self.get_queryset(request.user.id)
        serializer = UserShowSerializer(user_shows, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class ShowInfo(APIView):
    def get_queryset(self, show_id):
        show_info = get_object_or_404(Show, id=show_id)
        return show_info

    def get(self, request, *args, **kwargs):
        show_info = self.get_queryset(kwargs['show_id'])
        serializer = ShowSerializer(show_info)
        return Response(serializer.data)

    permission_classes = ()


class AddUserShow(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data['show_id'], request.user.id)
        if add_usershow_from_web(request.user.id, request.data['show_id']):
            return Response({'response': 'ok'})
        return Response({'response': 'error'})
    permission_classes = (IsAuthenticated, )
