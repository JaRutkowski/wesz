from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'reservations'

urlpatterns = [
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^create/$', login_required(views.CreateView.as_view()), name='create'),
    url(r'^(?P<pk>[0-9]+)/accept/$', login_required(views.accept), name='accept'),
    url(r'^(?P<pk>[0-9]+)/reject/$', login_required(views.reject), name='reject'),
]
