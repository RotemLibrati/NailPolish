from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=100, default="")
    last_met = models.DateTimeField(default=datetime(2000,1,1))

    def __str__(self):
        return self.user

class Notifications(models.Model):
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)