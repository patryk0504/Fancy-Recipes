from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm, UsernameUpdateForm, EmailUpdateForm


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

def profile(request):
    template = loader.get_template('profile.html')
    username_form = UsernameUpdateForm()
    email_form = EmailUpdateForm()


    context = {
        'username_form' : username_form,
        'email_form' : email_form,
        # placeholders
        'role' : 'tmpRole',
        'join_date' : '11-11-2021'
    }
    return HttpResponse(template.render(context, request))