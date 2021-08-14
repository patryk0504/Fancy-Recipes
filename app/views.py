from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import ListView

from django.core.exceptions import ObjectDoesNotExist


from .forms import (RegisterForm, ProfileUpdateForm, ProfileDeleteForm,
                    CreateIngredientForm, RecipeForm, CommentForm, AddSolidUnitForm,
                    AddLiquidUnitForm, EditIngredientForm)
from .models import Ingredient, Recipe, Account, Comment, LiquidUnits, SolidUnits
from .utils import UnitCalculator


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # tworzenie account dla usera
            this_user = User.objects.get(username=form.cleaned_data['username'])
            Account.objects.create(name=this_user.username, user_id=this_user.id)
            messages.info(request, "Account created successfully, please log in.")
            return redirect('login')
        else:
            messages.error(request, "Account cannot be created, some problems occurred.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    template = loader.get_template('profile.html')
    current_user = User.objects.get(id=request.user.id)
    account = Account.objects.get(user_id=current_user.id)

    comments = Comment.objects.all()
    recipes = Recipe.objects.all()

    num_of_comments = comments.filter(author=current_user).count()
    num_of_recipes = recipes.filter(author=current_user).count()

    context = {
        'role': account.role,
        'join_date': current_user.date_joined,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'job': account.job,
        'about_me': account.description,
        'stats': {'recipes_num': num_of_recipes,
                  'comments_num': num_of_comments,
                  },
    }
    return HttpResponse(template.render(context, request))


@login_required
def updateProfile(request):
    current_user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user_id=current_user.id)
            if form.cleaned_data['first_name']:
                current_user.first_name = form['first_name'].value()
            if form.cleaned_data['last_name']:
                current_user.last_name = form['last_name'].value()
            if form.cleaned_data['username']:
                current_user.username = form['username'].value()
            if form.cleaned_data['email']:
                current_user.email = form['email'].value()
            if form.cleaned_data['about']:
                account.description = form['about'].value()
            current_user.save()
            account.save()
            messages.info(request, "Profile successfully updated.")
            return redirect('.')
        else:
            messages.error(request, "Profile cannot be updated, some problems occurred.")
    else:
        form = ProfileUpdateForm()

    return render(request, "updateProfile.html", {"profile_form": form})


@login_required
def deleteProfile(request):
    current_user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = ProfileDeleteForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(user_id=current_user.id)
            current_user.delete()
            account.delete()
            return redirect('register')
        else:
            messages.error(request, "Profile cannot be deleted, some problems occurred.")
    else:
        form = ProfileDeleteForm()

    return render(request, "deleteProfile.html", {"delete_form": form})


# Handling ingredients
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


@login_required
def edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    if request.method == "POST":
        form = EditIngredientForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['name']:
                ingredient.name = form.cleaned_data['name']
            if form.cleaned_data['carbohydrate']:
                ingredient.carbohydrate = form.cleaned_data['carbohydrate']
            if form.cleaned_data['energy']:
                ingredient.energy = form.cleaned_data['energy']
            if form.cleaned_data['protein']:
                ingredient.protein = form.cleaned_data['protein']
            if form.cleaned_data['fat']:
                ingredient.fat = form.cleaned_data['fat']
            if form.cleaned_data['price']:
                ingredient.price = form.cleaned_data['price']
            ingredient.save()
            messages.info(request, "Ingredient updated")
            return redirect('ingredient-edit', ingredient_id)
        else:
            messages.error(request, "Cannot update chosen ingredient")
    else:
        form = EditIngredientForm()

    return render(request, "edit_ingredient.html", {"edit_ingredient_form": form, "ingredient": ingredient})


def delete_ingredient(request, ingredient_id):
    if request.method == "POST":
        ingredient = Ingredient.objects.get(id=ingredient_id)
        ingredient.delete()
        return redirect('ingredient-list')

    return render(request, "delete_ingredient.html")


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
def edit_recipe(request, recipe_id):
    if request.method == "GET":
        recipe_to_edit = Recipe.objects.filter(id=recipe_id).first()
        if not recipe_to_edit:
            messages.error(request, f"Not found recipe with id={recipe_id}.")
            return redirect('index')
        recipe_author = recipe_to_edit.author
        if recipe_author.id == request.user.id:
            form = RecipeForm(instance=recipe_to_edit)
            return render(request, 'recipe_edit.html', {'form': form})

        else:
            messages.error(request, "You have no permission to do that action.")
            return redirect('recipe_page', recipe_id)

    elif request.method == "POST":
        recipe_to_edit = Recipe.objects.filter(id=recipe_id).first()
        form = RecipeForm(request.POST, instance=recipe_to_edit)

        if form.is_valid():
            form.save()
            messages.info(request, "Recipe successfully edited.")
            return redirect('recipe_page', recipe_id)

        else:
            messages.error(request, "Unable to edit recipe")
            return redirect('recipe_page', recipe_id)


@login_required
def recipe_delete(request, recipe_id):
    if request.method == "GET":
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
        user = User.objects.get(id=request.user.id)
        commented_recipe = Recipe.objects.get(id=recipe_id)
        comment = Comment(last_edited=datetime.now(), author=user, recipe=commented_recipe)
        form = CommentForm(request.POST, instance=comment)

        if (form.is_valid()):
            comment.text = form.cleaned_data['text']
            comment.save()
            messages.info(request, "Comment added")
            return redirect('add-comment', recipe_id)

    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'recipe_id': recipe_id})


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
    accounts = Account.objects.all()
    comments = Comment.objects.all()
    recipes = Recipe.objects.all()
    num_of_comments = {}
    num_of_recipes = {}
    for account in accounts:
        num_of_comments[account.pk] = comments.filter(author=account.pk).count()
        num_of_recipes[account.pk] = recipes.filter(author=account.pk).count()
    # print(num_of_comments.values())

    print(num_of_comments)
    if (request.method == "GET"):
        return render(request, 'users.html',
                      {'users': accounts, 'num_of_comments': num_of_comments, 'num_of_recipes': num_of_recipes})


# Handling units
def add_unit(request):
    if request.method == "POST":
        if 'add_liquid' in request.POST:
            form1 = AddLiquidUnitForm(request.POST)
            if form1.is_valid():
                try:
                    LiquidUnits.objects.get(unit=form1.cleaned_data['unit'])
                    messages.info(request, "Such liquid unit already exists in the database.")
                except ObjectDoesNotExist:
                    form1.save()
                    messages.info(request, "Liquid unit successfully added to the database.")
                return redirect('.')
            else:
                messages.error(request, "Liquid unit cannot be added to the database, some problems occurred.")
        elif 'add_solid' in request.POST:
            form2 = AddSolidUnitForm(request.POST)
            if form2.is_valid():
                try:
                    SolidUnits.objects.get(unit=form2.cleaned_data['unit'])
                    messages.info(request, "Such solid unit already exists in the database.")
                except ObjectDoesNotExist:
                    form2.save()
                    messages.info(request, "Solid unit successfully added to the database.")
                return redirect('.')
            else:
                messages.error(request, "Solid unit cannot be added to the database, some problems occurred.")
    else:
        form1 = AddLiquidUnitForm()
        form2 = AddSolidUnitForm()

    return render(request, "add_unit.html", {"form1": form1, "form2": form2})


def unit_calculator(request):
    liquid = []
    liquidUnits = LiquidUnits.objects.all()
    for x in liquidUnits:
        liquid.append(x.unit)
    solid = []
    solidUnits = SolidUnits.objects.all()
    for y in solidUnits:
        solid.append(y.unit)
    context = {'liquid_units': liquid,
               'solid_units': solid
               }
    if request.method == "GET":
        return render(request, 'unit_calculator.html', context)


def calculate(request):
    result = UnitCalculator.convertHelper(request.GET["fromUnitName"], request.GET["toUnitName"], request.GET["amount"])
    return HttpResponse(result)



from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse


def autocompleteIngredients(request):
    if 'term' in request.GET:
        matched_ingredients = Ingredient.objects.filter(name__icontains=request.GET.get('term'))
        ingredients = [ingredient.name for ingredient in matched_ingredients]
        return JsonResponse(ingredients, safe=False)


def filterRecipes(request):
    if request.method == "POST":
        ingredients_names = request.POST.getlist("content[]")
        ingredients_list = [Ingredient.objects.get(name=ingredient_name) for ingredient_name in ingredients_names]
        filtered_recipes = Recipe.objects.all().filter(ingredients__in=ingredients_list).annotate(
            ingredient_count=Count('ingredients')).filter(ingredient_count=len(ingredients_list))
        filtered_recipes_ids = [str(recipe.id) for recipe in filtered_recipes]
        delimiter = ","
        filtered_recipes_ids = delimiter.join(filtered_recipes_ids)

        result_url = reverse('recipe-list')
        if filtered_recipes_ids != '':
            result_url = reverse('recipe-list-filter', args=[filtered_recipes_ids])
        elif len(ingredients_list) != 0:
            result_url = reverse('recipe-list-filter', args=["not_found"])

        return JsonResponse({
            'success': True,
            'url': result_url
        })


@login_required
def list_recipe(request, match=''):
    if request.method == "GET":
        if match == 'not_found':
            messages.info(request, "Recipes with specified ingredients are not found.")
            return render(request, 'list_recipe.html')

        recipes = Recipe.objects.all()
        if match != '':
            recipes_ids = [int(recipe_id) for recipe_id in match.split(",")]
            recipes = [recipe for recipe in recipes if recipe.id in recipes_ids]
        return render(request, 'list_recipe.html', {'recipes': recipes})


@login_required
def user_recipes(request):
    current_user = User.objects.get(id=request.user.id)
    recipes = Recipe.objects.filter(author=current_user)
    recipes = [recipe for recipe in recipes]
    return render(request, 'user_recipes.html', {'recipes': recipes})
