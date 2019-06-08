from django.contrib import admin

from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']


class UsersGroupAdmin(admin.ModelAdmin):
    list_display = ['group', 'leader']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['room', 'group', 'begin_date', 'end_date', 'status', 'requester', 'decider']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'status', 'read_on']


admin.site.register(Role)
admin.site.register(Room)
admin.site.register(Status)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UsersGroup, UsersGroupAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Notification, NotificationAdmin)
