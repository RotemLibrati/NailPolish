from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, UserProfile, Notifications
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Notifications)

