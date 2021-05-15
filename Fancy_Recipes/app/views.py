from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import HttpResponseNotFound


from .models import Ingredient, Recipe, Account, Comment, LiquidUnits, SolidUnits
from .forms import (RegisterForm, ProfileUpdateForm, ProfileDeleteForm,
                    CreateIngredientForm, DeleteIngredientForm, RecipeForm, CommentForm)
from .utils import UnitCalculator

from datetime import datetime
from django.contrib.auth.models import User


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
        'role': 'cook',
        'join_date': '11-11-2021',
        'full_name': 'Kenneth Valdez',
        'phone': '500 155 155',
        'job': 'McDonalds',
        'about_me': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi dictum ac lectus id efficitur',
        'stats': {'recipes_num': 10,
                  'comments_num': 20,
                  'likes': 30
                  },
    }
    return HttpResponse(template.render(context, request))


@login_required
def updateProfile(request):
    template = loader.get_template('updateProfile.html')
    profile_form = ProfileUpdateForm()
    context = {
        'profile_form': profile_form,
        'join_date': '11-11-2021',
        'full_name': 'Kenneth Valdez',
    }
    return HttpResponse(template.render(context, request))


@login_required
def deleteProfile(request):
    template = loader.get_template('deleteProfile.html')
    delete_form = ProfileDeleteForm()
    context = {
        'delete_form': delete_form
    }
    return HttpResponse(template.render(context, request))


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
        current_user = User.objects.get(id=request.user.id)
        new_recipe = Recipe(add_date=datetime.now(), author=current_user)
        form = RecipeForm(request.POST, instance=new_recipe)

        if form.is_valid():
            form.save()
            messages.info(request, "Receipe successfully added to the database.")
            return redirect('.')
    else:
        form = RecipeForm()

    return render(request, 'add_recipe.html', {'form': form})


@login_required
def list_recipe(request):
    if request.method == "GET":
        return render(request, 'list_recipe.html', {'recipes': Recipe.objects.all()})


@login_required
def edit_recipe(request, recipe_id):
    if request.method == "GET":
        instance = Recipe.objects.filter(id=recipe_id).first()
        if not instance:
            messages.error(request, f"Not found recipe with id={recipe_id}.")
            return redirect('index')
        recipe_author = instance.author
        if recipe_author.id == request.user.id:
            #TODO Obsługa edycji
            pass
        else:
            messages.error(request, "You have no permission to do that action.")
            return redirect('recipe_page', recipe_id)

    return redirect('recipe_page', recipe_id)


@login_required
def recipe_delete(request, recipe_id):
    if request.method == "POST":
        instance = Recipe.objects.filter(id=recipe_id).first()
        if not instance:
            messages.error(request, f"Not found recipe with id={recipe_id}.")
            return redirect('index')

        recipe_author = instance.author
        if recipe_author.id == request.user.id:
            instance.delete()
            messages.info(request, f"Recipe with id {recipe_id} deleted successfully.")
            return redirect('index')
        else:
            messages.error(request, "You have no permission to do that action.")
            return redirect('recipe_page', recipe_id)


@login_required
def recipe_page(request, recipe_id):
    if request.method == "GET":
        instance = Recipe.objects.filter(id=recipe_id).first()
        if instance:
            comments = Comment.objects.filter(recipe=recipe_id).all()
            return render(request, 'recipe_page.html', {'recipe': instance, 'comments': comments})
        else:
            messages.error(request, f"Not found recipe with id={recipe_id}.")
            return redirect('recipe_list')


@login_required
def add_comment(request, recipe_id):
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        comment = Comment(last_edited=datetime.now(), author=user, recipe=recipe_id)
        form = CommentForm(request.POST, instance=comment)

        if(form.is_valid()):
            comment.last_edited = form.cleaned_data['text']
            comment.save()
            messages.info(request, "Comment added")
            return redirect('.')
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form})


@login_required
def comment_delete(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.filter(id=comment_id).first()

        if not comment:
            messages.error(request, f"Comment with id={comment_id} was not found.")
            return redirect('index')

        if comment.author.id == request.user.id:
            comment.delete()
            messages.info(request, f"Comment was deleted.")
        else:
            messages.error(request, "You can delete only your comments.")

    return redirect('index')

def list_users(request):
    if(request.method == "GET"):
        return render(request, 'users.html', {'users': Account.objects.all()})

def unit_calculator(request):
    liquid = []
    liquidUnits = LiquidUnits.objects.all()
    for x in liquidUnits:
        liquid.append(x.unit)
    solid = []
    solidUnits = SolidUnits.objects.all()
    for y in solidUnits:
        solid.append(y.unit)
    context = {'liquid_units' : liquid,
               'solid_units' : solid
               }
    if request.method == "GET":
        return render(request, 'unit_calculator.html', context)

def calculate(request):
    result = UnitCalculator.convertHelper(request.GET["fromUnitName"], request.GET["toUnitName"], request.GET["amount"])
    return HttpResponse(result)
