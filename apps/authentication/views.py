# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.http import JsonResponse

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


@login_required(login_url="/login/")
def get_users(request):

            # username = form.cleaned_data['username']
            # password = form.cleaned_data["password1"]
            # user = authenticate(username=username, password=password)
            # login(request, user)
            # return redirect('user_list')
    userlist = list(User.objects.values())
    # for user in list(userlist):
    for user in userlist:
        del user["password"]
    print(userlist)
    form = RegisterForm()
    # if request.errors:
    print(request)
    context = {"users": userlist, "form": form, "message": ""}
    
    return render(request, "accounts/adduser.html", context)


@login_required(login_url="/login/")
def create_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            # password = form.cleaned_data["password1"]
            # user = authenticate(username=username, password=password)
            # login(request, user)
            message = "User Created Successfully"
            print(message)
            # request.method="GET"
            form = RegisterForm()
            result = "success"
        else:

            message = form.errors
            result = "error"
            print(message)
        return JsonResponse({"status": "success",  "message": message, "result": result })