from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

# TODO: remove
from django.views.generic.base import TemplateView


class ComingView(TemplateView):
    template_name = 'coming.html'


urlpatterns = patterns('',
    # Examples:
    url(r'^$', ComingView.as_view(), name='home'),
    url(r'^', include('cookiecutters.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
