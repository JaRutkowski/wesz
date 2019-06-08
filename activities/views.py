from django.views import generic

from reservations.models import *


class IndexView(generic.ListView):
    """
    View for the accepted reservations of the group which the user belongs to.
    """
    template_name = 'activities/index.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        """
        Returns a list of all of the rooms.
        """
        return Room.objects.order_by('name')

    def get_context_data(self, **kwargs):
        """
        Supplements the context of a number of the user's notifications
        and a list of all accepted reservations of the group which the user belongs to.
        """
        user = self.request.user
        groups = user.groups.all()
        if user.is_authenticated:
            user_profile = UserProfile.objects.get(user=user)

        context = super(IndexView, self).get_context_data(**kwargs)
        if user.is_authenticated:
            context['unread_counter'] = Notification.objects \
                .filter(recipient=user_profile) \
                .filter(read_on__isnull=True).count()

        context['group_reservation_list'] = Reservation.objects \
            .filter(group__group__in=groups) \
            .filter(status__name__contains="Accepted")\
            .order_by('-begin_date')

        return context
