from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ingredient, Recipe, SolidUnits, LiquidUnits
from searchableselect.widgets import SearchableSelect

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileUpdateForm(forms.ModelForm):
    last_name = forms.CharField(required=False, max_length=150)
    first_name = forms.CharField(required=False, max_length=150)
    username = forms.CharField(required=False, max_length=150)
    email = forms.EmailField(required=False, max_length=254)
    about = forms.CharField(widget=forms.Textarea, help_text='400 characters max.', max_length=400, required=False)

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


class DeleteIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "price"]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "add_date", "author", "ingredients"]
        exclude = ["author", "add_date"]


class CommentForm(forms.ModelForm):
    class Meta:
        fields = ["text"]
        exclude = ["author", "last_edited", "recipe"]


class AddSolidUnitForm(forms.ModelForm):
    conversionFactorToMainUnit = forms.FloatField(required=True, min_value=0.0)
    unit = forms.CharField(max_length=10, required=True)

    class Meta:
        model = SolidUnits
        fields = ["unit", "conversionFactorToMainUnit"]


class AddLiquidUnitForm(forms.ModelForm):
    conversionFactorToMainUnit = forms.FloatField(required=True, min_value=0.0)
    unit = forms.CharField(max_length=10, required=True)

    class Meta:
        model = LiquidUnits
        fields = ["unit", "conversionFactorToMainUnit"]


class DeleteLiquidUnitForm(forms.ModelForm):
    unit = forms.CharField(max_length=10, required=True)

    class Meta:
        model = LiquidUnits
        fields = ["unit"]


class DeleteSolidUnitForm(forms.ModelForm):
    unit = forms.CharField(max_length=10, required=True)

    class Meta:
        model = SolidUnits
        fields = ["unit"]


class EditLiquidUnitForm(forms.ModelForm):
    old_unit = forms.CharField(max_length=10, required=True)
    new_unit = forms.CharField(max_length=10, required=True)
    new_factor = forms.FloatField(required=True, min_value=0.0)

    class Meta:
        model = LiquidUnits
        fields = ["old_unit", "new_unit", "new_factor"]


class EditSolidUnitForm(forms.ModelForm):
    old_unit = forms.CharField(max_length=10, required=True)
    new_unit = forms.CharField(max_length=10, required=True)
    new_factor = forms.FloatField(required=True, min_value=0.0)

    class Meta:
        model = SolidUnits
        fields = ["old_unit", "new_unit", "new_factor"]







from dal import autocomplete
class FilterRecipesForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('ingredients',)
        widgets = {
            'ingredients': autocomplete.ModelSelect2Multiple(url='ingredient-autocomplete')
        }
