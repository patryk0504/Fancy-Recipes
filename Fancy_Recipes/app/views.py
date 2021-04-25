from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm, CreateIngredientForm, DeleteIngredientForm
from django.views.generic import ListView
from .models import Ingredient


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

