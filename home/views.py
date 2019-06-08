from django.views import generic

from reservations.models import *


class IndexView(generic.ListView):
    """
    View for the general description of this web application.
    """
    template_name = 'home/index.html'
    context_object_name = 'home_list'

    def get_queryset(self):
        """
        Returns a list of all of the rooms.
        """
        return Room.objects.order_by('name')

    def get_context_data(self, **kwargs):
        """
        Supplements the context of a number of the user's notifications.
        """
        user = self.request.user
        if user.is_authenticated:
            user_profile = UserProfile.objects.get(user=user)

        context = super(IndexView, self).get_context_data(**kwargs)
        if user.is_authenticated:
            context['unread_counter'] = Notification.objects \
                .filter(recipient=user_profile) \
                .filter(read_on__isnull=True).count()

        return context
