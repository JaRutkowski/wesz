from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import generic

from reservations.models import *


class IndexView(generic.ListView):
    """
    View for the user's notifications.
    """
    template_name = 'notifications/index.html'
    context_object_name = 'notification_list'

    def get_queryset(self):
        """
        Returns a list of all of the user's notifications.
        """
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        return Notification.objects.filter(recipient=user_profile).order_by('-id')

    def get_context_data(self, **kwargs):
        """
        Supplements the context of a number of the user's notifications.
        """
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['unread_counter'] = Notification.objects \
            .filter(recipient=user_profile) \
            .filter(read_on__isnull=True).count()
        return context


def mark_all_as_read(request):
    """
    Mark all unread user's notifications as read at the current datetime.
    """
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    notifications = Notification.objects.filter(recipient=user_profile)
    now = datetime.now()

    for notification in notifications:
        if notification.read_on is None:
            notification.read_on = now
            notification.save()

    return HttpResponseRedirect(reverse('notifications:index'))
