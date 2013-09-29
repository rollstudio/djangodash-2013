from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

from django.views.generic.base import TemplateView


class GithubCallbackView(TemplateView):
    template_name = 'github_callback.html'


urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^github/callback/$', GithubCallbackView.as_view(), name='github_callback'),
    url(r'^', include('cookiecutters.urls')),
)
