from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Ingredient


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "price"]


class DeleteIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "price"]
