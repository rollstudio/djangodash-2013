from django.conf.urls import patterns, include, url

from .views import CookieGeneratorView

urlpatterns = patterns('',
    # Examples:
    url(r'(?P<pk>\d+)/$', CookieGeneratorView.as_view()),
)
