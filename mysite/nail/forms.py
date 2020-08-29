from django import forms
from .models import User, UserProfile


class LoginForm(forms.Form):
    user_name = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput(), initial='')
