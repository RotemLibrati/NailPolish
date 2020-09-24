
from datetime import datetime, timezone
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, Http404
from django.template.context_processors import csrf
from django.urls import reverse
from django.utils.datetime_safe import datetime

from .forms import LoginForm, CompleteUserForm, ProfileForm, MeetingForm
from .models import User, UserProfile, Meeting
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.template import RequestContext



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
            return render(request, 'nail/profile-details.html')
    else:
        user = User.objects.get(username=username)
        form = ProfileForm()
    context = {'user': user, 'form': form}
    return render(request, 'nail/new-profile.html', context)


def profile(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponse("Not logged in")
    user = request.user
    up1 = UserProfile.objects.get(user=user)
    now = datetime.now(timezone.utc)
    print(up1.next_meeting)
    if(up1.next_meeting < now):
        up1.next_meeting = ""
    context = {'user': user, 'up1': up1}
    return render(request, 'nail/profile-details.html', context)


def logout(request):
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = AnonymousUser()
    return HttpResponseRedirect(reverse('nail:index'))


def success(request):
    return render(request, 'nail/success.html')


def meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            orderly = True
            day = form.cleaned_data.get('day')
            month = form.cleaned_data.get('month')
            year = form.cleaned_data.get('year')
            hour = form.cleaned_data.get('hour')
            up1 = UserProfile.objects.get(user=request.user)
            defult_date= datetime.strptime('01/01/20 00:00:00', '%m/%d/%y %H:%M:%S')
            if "_make-unique" in request.POST:
                print(up1.exist_meeting)
                #up1.next_meeting = defult_date
                up1.exist_meeting = False
                print("after")
                print(up1.exist_meeting)
                up1.save()
                meet = Meeting(date=defult_date, user=up1)
                meet.save()
                return render(request, 'nail/success.html')
            if (month==2 and (day==29 or day==30 or day==31)):
                orderly = False
                return render(request, 'nail/not-success.html')
            elif (month==4 and day == 31):
                orderly = False
                return render(request, 'nail/not-success.html')
            elif (month == 6 and day ==31):
                orderly = False
                return render(request, 'nail/not-success.html')
            elif (month == 9 and day == 31):
                orderly = False
                return render(request, 'nail/not-success.html')
            elif ( month==11 and day == 31):
                orderly = False
                return render(request, 'nail/not-success.html')
            elif up1.exist_meeting == True:
                orderly = False
                return render(request, 'nail/not-success.html')
            else:
                date = '{0}/{1}/{2} {3}'.format(month, day, year, hour)
                datetime_object = datetime.strptime(date, '%m/%d/%y %H:%M:%S')
                if(datetime_object<datetime.now()):
                    orderly=False
                    return render(request, 'nail/not-success.html')
                up1.next_meeting = datetime_object
                up1.exist_meeting = True
                up1.save()
                print(orderly)
                if(orderly):
                    print("in%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    meet = Meeting(date=datetime_object, user=up1)
                    meet.save()
                return HttpResponseRedirect(reverse('nail:success'))

    else:
        form = MeetingForm()
    context = {'form': form}
    return render(request, 'nail/meeting.html', context)


def not_success(request):
    return render(request, 'nail/not-success.html')


def pictures(request):
    return render(request, 'nail/pictures.html')


def meeting_admin(request):
    user = request.user
    meet = (Meeting.objects.all())
    print(meet)
    context = {'user': user, 'meet': meet}
    return render(request, 'nail/meeting-admin.html', context)