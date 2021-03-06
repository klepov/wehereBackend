__author__ = 'dima'
from django.forms import widgets
from rest_framework import serializers
from .models import Parent,Children


class SnippetSerializerParent(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = ("device_ID", "latitude", "longitude")

class SnippetSerializerChildren(serializers.ModelSerializer):

    class Meta:
        model = Children
        fields = ("device_ID", "latitude", "longitude")



