from django.conf.urls import patterns, include, url

from cookiecutters import views

urlpatterns = patterns('',
    # Examples:
    #url(r'cookies/(?P<pk>\d+)/$', views.CookieGeneratorView.as_view()),
    url(r'(\w+)/(\w+)/$', views.cookiecutter_detail),
    url(r'(\w+)/(\w+)/bake$', views.bake),
)
