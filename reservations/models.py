from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Role(models.Model):
    """
    Model representing the role it plays the UserProfile.

    :Fields:
        **name**
        *(string)*
            Name of role.
            For example:
                * Administrator,
                * Professor,
                * Student.
    """
    name = models.CharField(_('role'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class Room(models.Model):
    """
    Model representing the room at the faculty, which can be reserved in order to peform the exam.

    :Fields:
        **name**
        *(string)*
            Name of room, for example: 401.
    """
    name = models.CharField(_('room'),max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')


class Status(models.Model):
    """
    Model representing the status of reservation.

    :Fields:
        **name**
        *(string)*
            Name of status.
            For example:
                * Waiting,
                * Accepted,
                * Rejected.
    """
    name = models.CharField(_('status'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')


class UserProfile(models.Model):
    """
    Model representing the extended information about user.

    :Fields:
        **user**
        *(django.contrib.auth.models.User)*
            Instance of existing User account.

        **role**
        *(models.Role)*
            The role which plays the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, verbose_name=_('role'))

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')


class UsersGroup(models.Model):
    """
    Model representing the extended information about students' group.

    :Fields:
        **group**
        *(django.contrib.auth.models.Group)*
            Instance of existing Group.

        **leader**
        *(models.UserProfile)*
            Leader of the students' group.
    """
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    leader = models.ForeignKey(UserProfile, null=True, blank=True, default=None, verbose_name=_('leader'))

    def __str__(self):
        return self.group.__str__()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')


class Reservation(models.Model):
    """
    Model representing the information about reservation of room.

    :Fields:
        **room**
        *(models.Room)*
            The room to which the reservation refers.

        **group**
        *(models.UsersGroup)*
            The students' group to which the reservation refers.

        **begin_date**
        *(datetime)*
            The beginning date of the reservation.

        **end_date**
        *(datetime)*
            The ending date of the reservation, cannot be earlier than beginning date.

        **status**
        *(models.Status)*
            The current status about the reservation request.

        **requester**
        *(models.UserProfile)*
            User which consists the reservation request.

        **decider**
        *(models.UserProfile)*
            User which accepts or rejects the reservation request.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_('room'))
    group = models.ForeignKey(UsersGroup, on_delete=models.CASCADE, verbose_name=_('group'))
    begin_date = models.DateTimeField(_('begin date'))
    end_date = models.DateTimeField(_('end date'))
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=_('status'))
    requester = models.ForeignKey(UserProfile, related_name="requester", verbose_name=_('requester'))
    decider = models.ForeignKey(UserProfile, related_name="decider", null=True, blank=True, default=None, verbose_name='decider')

    def __str__(self):
        return self.id.__str__()

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')


class Notification(models.Model):
    """
    Model representing the information about notification of UserProfile.

    :Fields:
        **sender**
        *(models.UserProfile)*
            User which creates the notification during doing operations related to the reservation request.

        **recipient**
        *(models.UserProfile)*
            User which receives the notification information related to operations on the reservation request.

        **status**
        *(models.Status)*
            The status about the reservation request related to the notification.

        **read_on**
        *(datetime)*
            The date of user confirmation of read the reservation.

        **is_unread()**
        *(function)*
            The function describing whether the notification is not read.
    """
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender", verbose_name=_('sender'))
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="recipient", verbose_name=_('recipient'))
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=_('status'))
    read_on = models.DateTimeField(_('read on'), null=True, blank=True, default=None)

    def __str__(self):
        return self.id.__str__()

    def is_unread(self):
        return self.read_on is None

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
