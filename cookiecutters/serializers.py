from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import CookieCutter


class NaiveSerializer(serializers.WritableField):
    def to_native(self, obj):
        return obj


class BakeHyperlinkField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        user = getattr(obj, 'user', None)
        name = getattr(obj, 'name', None)

        kwargs = {
            'username': user.username,
            'cookie': name
        }

        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class CookieCutterSerializer(serializers.HyperlinkedModelSerializer):
    # not sure why without this was returning a string
    tags = NaiveSerializer('tags')
    options = NaiveSerializer('options')
    baking_url = BakeHyperlinkField(view_name='bake_cookie')

    class Meta:
        model = CookieCutter
        fields = ('id', 'name', 'description', 'url',
                  'options', 'language', 'tags', 'baking_url')
