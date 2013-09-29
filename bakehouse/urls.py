from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

# TODO: remove
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^', include('cookiecutters.urls')),
)
