from django.conf.urls import patterns, url

from cookiecutters import views

urlpatterns = patterns('',
    url(r'cookies/$', views.CookieListView.as_view()),
    url(r'(?P<username>\w+)/(?P<cookie>\w+)/bake/$', views.BakeCookieView.as_view()),
    url(r'(?P<username>\w+)/(?P<cookie>\w+)/$', views.JSONBakeView.as_view()),
)
