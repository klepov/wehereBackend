from django.contrib.auth.models import User

__author__ = 'dima'
from django.forms import widgets
from rest_framework import serializers
from core.models import Parent,Children


class SnippetSerializerParent(serializers.ModelSerializer):

    class Meta:
        model = User
        # field = ("username","password")

