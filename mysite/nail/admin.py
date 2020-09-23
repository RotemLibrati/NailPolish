from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Users, UserProfile, Notifications, Meeting
admin.site.register(Users)
admin.site.register(UserProfile)
admin.site.register(Notifications)
admin.site.register(Meeting)


