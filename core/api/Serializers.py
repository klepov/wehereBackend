from rest_framework import serializers

from core.models import CommonData, Parent


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ('image_user',)