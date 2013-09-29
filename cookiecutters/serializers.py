from rest_framework import serializers

from .models import CookieCutter


class NaiveSerializer(serializers.WritableField):
    def to_native(self, obj):
        return obj


class CookieCutterSerializer(serializers.ModelSerializer):
    # not sure why without this was returning a string
    tags = NaiveSerializer('tags')
    options = NaiveSerializer('options')

    class Meta:
        model = CookieCutter
        fields = ('id', 'name', 'description', 'url',
                  'options', 'language', 'tags')
