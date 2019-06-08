import datetime

from django.test import TestCase
from django.urls import reverse

from reservations.models import *


def create_reservation(status_name):
    """
    Creates a reservation with the given `status_name`.
    """
    room = Room.objects.create(name="test_room")
    auth_group = Group.objects.create(name="test_group")
    group = UsersGroup.objects.create(group=auth_group)
    begin_date = datetime.datetime(2016, 12, 14, 8, 30, 0, tzinfo=datetime.timezone.utc)
    end_date = begin_date + datetime.timedelta(minutes=90)
    status = Status.objects.create(name=status_name)
    auth_user = User.objects.create(username="test", email="test@test.com", password="test1test")
    role = Role.objects.create(name="test_role")
    requester = UserProfile.objects.create(user=auth_user, role=role)
    return Reservation.objects.create(room=room, group=group,
                                      begin_date=begin_date, end_date=end_date,
                                      status=status, requester=requester)


class RoomsViewTests(TestCase):
    """
    Set of tests related to viewing index page of rooms.
    """
    def test_index_view_with_no_rooms(self):
        """
        If no rooms exist, none of them should be displayed on the index page.
        """
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['room_list'], [])

    def test_index_view_with_two_rooms(self):
        """
        The index page may display multiple rooms.
        """
        Room.objects.create(name="room1")
        Room.objects.create(name="room2")
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['room_list'], ['<Room: room1>', '<Room: room2>'])

    def test_index_view_with_no_reservations(self):
        """
        If no reservations exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], [])

    def test_index_view_with_a_waiting_reservation(self):
        """
        Waiting reservation should not be displayed on the index page.
        """
        create_reservation("Waiting")
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], [])

    def test_index_view_with_a_accepted_reservation(self):
        """
        Accepted reservation should be displayed on the index page.
        """
        create_reservation("Accepted")
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], ['<Reservation: 1>'])

    def test_index_view_with_a_rejected_reservation(self):
        """
        Rejected reservation should not be displayed on the index page.
        """
        create_reservation("Rejected")
        response = self.client.get(reverse('rooms:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], [])
