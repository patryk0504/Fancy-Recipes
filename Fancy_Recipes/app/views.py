from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm, ProfileDeleteForm
from django.contrib.auth.decorators import  login_required


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Account created successfully, please log in.")
            return redirect(login)
        else:
            messages.error(request, "Account cannot be created, some problem occurred.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def profile(request):
    template = loader.get_template('profile.html')
    context = {
        # placeholders
        'role' : 'cook',
        'join_date' : '11-11-2021',
        'full_name' : 'Kenneth Valdez',
        'email' : 'user12345@gmail.com',
        'phone' : '500 155 155',
        'job' : 'McDonalds',
        'about_me' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi dictum ac lectus id efficitur',
    }
    return HttpResponse(template.render(context, request))

@login_required
def updateProfile(request):
    template = loader.get_template('updateProfile.html')
    profile_form = ProfileUpdateForm()
    context = {
        'profile_form' : profile_form,
        'join_date': '11-11-2021',
        'full_name': 'Kenneth Valdez',
    }
    return HttpResponse(template.render(context,request))

@login_required
def deleteProfile(request):
    template = loader.get_template('deleteProfile.html')
    delete_form = ProfileDeleteForm()
    context = {
        'delete_form' : delete_form
    }
    return HttpResponse(template.render(context,request))