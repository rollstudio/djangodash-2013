from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# TODO: remove
from django.views.generic.base import TemplateView


class ComingView(TemplateView):
    template_name = 'coming.html'


urlpatterns = patterns('',
    # Examples:
    url(r'^$', ComingView.as_view(), name='home'),
    # url(r'^bakehouse/', include('bakehouse.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
