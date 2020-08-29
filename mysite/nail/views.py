from django.contrib.auth import authenticate
from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm

from .models import User, UserProfile

from django.shortcuts import render

from django.contrib.auth import authenticate, login


def index(request):
    context = {}
    return HttpResponse("sssssss")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                user = request.user
                userprofile = UserProfile.object.get(user=user)
                return render(request, 'nail/login.html')
            return render(request, 'nail/login.html')
        else:
            form = LoginForm()
            context = {'form' : form}
            return render(request, 'nail/login.html', context)
    else:
        return render(request, 'nail/login.html')