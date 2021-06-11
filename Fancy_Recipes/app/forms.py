from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Ingredient, Recipe, SolidUnits, LiquidUnits, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileUpdateForm(forms.ModelForm):
    last_name = forms.CharField(required=False, max_length=150, label="Nazwisko")
    first_name = forms.CharField(required=False, max_length=150, label="Imie")
    username = forms.CharField(required=False, max_length=150, label="Nazwa użytkownika")
    email = forms.EmailField(required=False, max_length=254)
    about = forms.CharField(widget=forms.Textarea, help_text='400 characters max.', max_length=400, required=False, label="O mnie")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'about']


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []  # Form has only submit button.  Empty "fields" list still necessary, though.


class CreateIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "price"]
        labels = {"name": "nazwa składnika", "price": "cena"}


class DeleteIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = []


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "add_date", "author", "ingredients"]
        exclude = ["author", "add_date"]
        labels = {"name": "nazwa przepisu", "description": "opis", "ingredients": "składniki"}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = ["treść komentarza"]
        exclude = ["author", "last_edited", "recipe"]


class AddSolidUnitForm(forms.ModelForm):
    conversionFactorToMainUnit = forms.FloatField(required=True, min_value=0.0, label="Współczynnik konwersji")
    unit = forms.CharField(max_length=10, required=True, label="Jednostka")

    class Meta:
        model = SolidUnits
        fields = ["unit", "conversionFactorToMainUnit"]


class AddLiquidUnitForm(forms.ModelForm):
    conversionFactorToMainUnit = forms.FloatField(required=True, min_value=0.0, label="Współczynnik konwersji")
    unit = forms.CharField(max_length=10, required=True, label="Jednostka")

    class Meta:
        model = LiquidUnits
        fields = ["unit", "conversionFactorToMainUnit"]


class EditIngredientForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=False, label="Nazwa")
    carbohydrate = forms.FloatField(required=False, label="Węglowodany")
    energy = forms.FloatField(required=False, label="Kalorie")
    protein = forms.FloatField(required=False, label="Białko")
    fat = forms.FloatField(required=False, label="Tłuszcze")
    price = forms.DecimalField(required=False, label="Cena")

    class Meta:
        model = Ingredient
        fields = ["name", "carbohydrate", "energy", "protein", "fat", "price"]
