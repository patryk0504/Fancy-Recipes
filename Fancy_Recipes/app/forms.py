from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(required=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    about = forms.CharField(widget=forms.Textarea, help_text='400 characters max.', max_length=400, required=False)

    class Meta:
        model = User
        fields = ['full_name','username', 'email', 'about']
