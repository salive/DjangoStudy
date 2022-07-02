from rest_framework import serializers
from .models import Show, UserShows
from django.contrib.auth.models import User


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'title', 'year',
                  'poster', 'description', 'rating', 'is_series')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserShows
        fields = ('show_id', )
