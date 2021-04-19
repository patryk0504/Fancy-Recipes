from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))