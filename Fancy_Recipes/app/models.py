from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = [("U", 'user'), ("A", 'admin'), ("C", 'cook')]

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, blank = False)
    join_date = models.DateField(auto_now_add = True, blank = True)
    role = models.CharField(max_length = 1, choices = ACCOUNT_TYPES, default = "U")

# all fields are calculated based on 100g of product
class Ingredient(models.Model):
    name = models.CharField(max_length = 200, blank = False)

    carbohydrate = models.FloatField(blank=True,default=0) 
    carbohydrate_units = models.CharField(max_length = 10, blank = True,default="")

    energy = models.FloatField(blank=True,default=0) 

    protein = models.FloatField(blank=True,default=0)
    protein_units = models.CharField(max_length = 10, blank = True,default="")

    fat = models.FloatField(blank=True,default=0)
    fat_units = models.CharField(max_length = 10, blank = True,default="")

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
