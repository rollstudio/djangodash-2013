from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('cookiecutters.urls')),
)
