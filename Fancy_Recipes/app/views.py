from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.views.generic import ListView
from .models import Ingredient, Recipe
from .forms import (RegisterForm, ProfileUpdateForm, ProfileDeleteForm,
                    CreateIngredientForm, DeleteIngredientForm, CreateRecipeForm)


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
            return redirect('login')
        else:
            messages.error(request, "Account cannot be created, some problem occurred.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    template = loader.get_template('profile.html')
    context = {
        # placeholders
        'role' : 'cook',
        'join_date' : '11-11-2021',
        'full_name' : 'Kenneth Valdez',
        'phone' : '500 155 155',
        'job' : 'McDonalds',
        'about_me' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi dictum ac lectus id efficitur',
        'stats' : {'recipes_num' : 10,
                   'comments_num' : 20,
                   'likes' : 30
                   },
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


def create_ingredient(request):
    if request.method == "POST":
        form = CreateIngredientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Ingredient successfully added to the database.")
            return redirect('.')
        else:
            messages.error(request, "Ingredient cannot be added to the database, some problems occurred.")
    else:
        form = CreateIngredientForm()

    return render(request, "create_ingredient.html", {"form": form})


def delete_ingredient(request):
    if request.method == "POST":
        form = DeleteIngredientForm(request.POST)

        get_name = request.POST.get('name')
        get_price = request.POST.get('price')
        records_to_delete = Ingredient.objects.filter(name=get_name, price=get_price)

        # form musi byc poprawny i musi istniec skladnik w bazie do usuniecia - inaczej error
        if form.is_valid() and len(list(records_to_delete)) > 0:
            records_to_delete.delete()
            messages.info(request, "Ingredient successfully deleted from the database.")
            return redirect('.')
        else:
            messages.error(request, "Ingredient cannot be deleted from the database, some problems occurred.")
    else:
        form = DeleteIngredientForm()

    return render(request, "delete_ingredient.html", {"form": form})


def list_ingredients(request):
    context = {
        'ingredients': Ingredient.objects.all()
    }
    return render(request, 'list_ingredient.html', context)


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'list_ingredient.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'ingredients'
    ordering = ['price']  # sortowanie po najnizszej


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = CreateRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Receipe successfully added to the database.")
            return redirect('.')
    else:
        form = CreateRecipeForm()

    return render(request, 'add_recipe.html', {'form': form})


@login_required
def list_recipe(request):
    if request.method == "GET":
        return render(request, 'list_recipe.html', {'recipes': Recipe.objects.all()})
