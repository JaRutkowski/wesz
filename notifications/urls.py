from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'notifications'

urlpatterns = [
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^mark_all_as_read/$', login_required(views.mark_all_as_read), name='mark_all_as_read'),
]
