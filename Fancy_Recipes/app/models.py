from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = [("U", 'user'), ("A", 'admin'), ("C", 'cook')]

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    join_date = models.DateField(auto_now_add = True, blank = True)
    role = models.CharField(max_length = 1, choices = ACCOUNT_TYPES, default = "U")


class Ingredient(models.Model):
    name = models.CharField(max_length = 50, blank = False)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)


class Recipe(models.Model):
    name = models.CharField(max_length = 50, blank = False)
    text = models.TextField(blank = False)
    add_date = models.DateField(auto_now_add = True, blank = True)
    author = models.ForeignKey(Account, on_delete = models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)

class Comment(models.Model):
    author = models.ForeignKey(Account, on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    text = models.TextField(blank = False)
