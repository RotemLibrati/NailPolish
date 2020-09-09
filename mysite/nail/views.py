from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse

from .forms import LoginForm, CompleteUserForm, ProfileForm
from .models import User, UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session


def index(request):
    context = {}
    if request.user is not None:
        context['user'] = request.user
    return render(request, 'nail/index.html', context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('nail:profile'))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'nail/login.html', context) #מועבר לדף זה לאחר לחיצה על התחברות בעמוד הקודם


def new_user(request):
    if request.method == 'POST':
        user_form = CompleteUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = get_object_or_404(User, username=user_form.cleaned_data['username'])
            return HttpResponseRedirect(reverse('nail:new-profile', args=[str(user.username)])) # לחיצה על כפתור submit תעביר אותי לקישור
    else: # מכניס אותי לדף עם הקישור למטה כי הוא עדיין לא זיהה form
        user_form = CompleteUserForm()
        context = {'user_form': user_form}
        return render(request, 'nail/new-user.html', context)


def new_profile(request, username):
    def attach_user(sender, **kwargs):
        userprofile = kwargs['instance']
        userprofile.user = user
        post_save.disconnect(attach_user, sender=UserProfile)
        userprofile.save()

    if request.method == 'POST':
        user = User.objects.get(username=username)
        form = ProfileForm(request.POST)
        if form.is_valid():
            post_save.connect(attach_user, sender=UserProfile)
            form.save()
            return render(request, 'nail/success.html')
    else:
        user = User.objects.get(username=username)
        form = ProfileForm()
    return render(request, 'nail/new-profile.html', {'user': user, 'form': form})


def profile(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    context ={user:'user'}
    return render(request, 'nail/profile-details.html')


def logout(request):
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return HttpResponseRedirect(reverse('nail:index'))


def success(request):
    return render(request, 'nail/success.html')