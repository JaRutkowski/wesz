from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from reservations.models import *


class IndexView(generic.ListView):
    """
    View for the reservation's management.
    """
    template_name = 'reservations/index.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        """
        Returns a list of all of the rooms.
        """
        return Room.objects.order_by('name')

    def get_context_data(self, **kwargs):
        """
        Supplements the context of a number of the user's notifications
        and the lists of user's reservations,
        already accepted or waiting reservations
        and the new reservation requests to manage.
        """
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        context = super(IndexView, self).get_context_data(**kwargs)

        context['unread_counter'] = Notification.objects \
            .filter(recipient=user_profile) \
            .filter(read_on__isnull=True).count()

        context['my_reservation_list'] = Reservation.objects \
            .filter(requester=user_profile) \
            .order_by('-begin_date')

        context['all_reservation_list'] = Reservation.objects \
            .filter(Q(status__name__contains="Accepted")
                    | Q(status__name__contains="Waiting"))\
            .order_by('room')

        if user_profile.role == Role.objects.get(name__contains="Administrator"):
            context['all_request_list'] = Reservation.objects \
                .order_by('-begin_date')
        else:
            context['all_request_list'] = Reservation.objects.none()

        return context


class ReservationForm(ModelForm):
    """
    Class for preparation a reservation to display in an editable form.
    """
    class Meta:
       model = Reservation
       fields = ['room', 'group', 'begin_date', 'end_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        user_profile = UserProfile.objects.get(user=user)
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = UsersGroup.objects.filter(leader=user_profile)

        if user_profile.role == Role.objects.get(name__contains="Administrator")\
            or user_profile.role == Role.objects.get(name__contains="Professor"):
            self.fields['group'].queryset = UsersGroup.objects.all()


class CreateView(generic.CreateView):
    """
    View for creating a new reservation request.
    """
    template_name = 'reservations/create.html'
    form_class = ReservationForm

    def get_context_data(self, **kwargs):
        """
        Supplements the context of a number of the user's notifications
        and the list of already accepted or waiting reservations.
        """
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        context = super(CreateView, self).get_context_data(**kwargs)

        context['unread_counter'] = Notification.objects \
            .filter(recipient=user_profile) \
            .filter(read_on__isnull=True).count()

        context['all_reservation_list'] = Reservation.objects \
            .filter(Q(status__name__contains="Accepted")
                    | Q(status__name__contains="Waiting"))\
            .order_by('room')
        context['room_list'] = Room.objects.order_by('name')


        return context

    def get_form_kwargs(self):
        """
        Provides information about current logged user to the ReservationForm.
        """
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        """
        Returns to the list of reservations after adding new one.
        """
        return reverse('reservations:index')

    def form_valid(self, form):
        """
        Validates and completes the reservation data before adding new one.
        """
        # Checking existing reservations
        reservations_of_room = Reservation.objects\
            .filter(room=form.instance.room) \
            .filter(Q(status__name__contains="Accepted")
                    | Q(status__name__contains="Waiting"))

        for reservation in reservations_of_room:
            if form.instance.begin_date < reservation.end_date and form.instance.end_date > reservation.begin_date:
                form.add_error("room", "Room has already reserved within the prescribed period")
                return super(CreateView, self).form_invalid(form)

        # Checking specified period
        if form.instance.begin_date >= form.instance.end_date:
            form.add_error("begin_date", "The specified period is incorrect")
            return super(CreateView, self).form_invalid(form)

        # If everything's ok, complete the reservation
        form.instance.status = Status.objects.get(name__contains="Waiting")
        form.instance.requester = UserProfile.objects.get(user=self.request.user)

        # And create the notifications
        administrators = UserProfile.objects.filter(role=Role.objects.get(name__contains="Administrator"))

        for administrator in administrators:
            Notification.objects.create(sender=form.instance.requester, recipient=administrator,
                                        status=Status.objects.get(name__contains="Waiting"))

        return super(CreateView, self).form_valid(form)


def accept(request, pk):
    """
    Changes status of given reservation to 'Accepted' and returns to the list of reservations.
    """
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.role != Role.objects.get(name__contains="Administrator"):
        return HttpResponse('Unauthorized', status=401)

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = Status.objects.get(name__contains="Accepted")
    reservation.decider = user_profile
    reservation.save()

    Notification.objects.create(sender=user_profile, recipient=reservation.requester, status=reservation.status)

    return HttpResponseRedirect(reverse('reservations:index'))


def reject(request, pk):
    """
    Changes status of given reservation to 'Rejected' and returns to the list of reservations.
    """
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.role != Role.objects.get(name__contains="Administrator"):
        return HttpResponse('Unauthorized', status=401)

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = Status.objects.get(name__contains="Rejected")
    reservation.decider = user_profile
    reservation.save()

    Notification.objects.create(sender=user_profile, recipient=reservation.requester, status=reservation.status)

    return HttpResponseRedirect(reverse('reservations:index'))
