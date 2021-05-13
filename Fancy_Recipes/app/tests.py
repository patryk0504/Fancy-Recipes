from .models import Account, Recipe, Ingredient
from django.contrib.auth.models import User
import unittest as ut
from datetime import datetime


from .forms import RecipeForm


# Create your tests here.

class AddRecipeFormTest(ut.TestCase):
    def test_Name_Field_Label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')
    def test_Description_Field_Label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Description')
    def test_Ingredients_Field_Label(self):
        form = RecipeForm()
        self.assertTrue(form.fields['ingredients'].label is None or form.fields['ingredients'].label == 'Ingredients')
    def test_AddDate_Field_Label_Should_Be_Excluded(self):
        form = RecipeForm()
        with self.assertRaises(KeyError) as raises:
            self.assertTrue(form.fields['add_date'].label is None or form.fields['add_date'].label == 'Add date')
    def test_Author_Field_Label_Should_Be_Excluded(self):
        form = RecipeForm()
        with self.assertRaises(KeyError) as raises:
            self.assertTrue(form.fields['author'].label is None or form.fields['author'].label == 'Author')

    def test_Form_is_invalid_Required_Values_Not_Provided(self):
        form_data = {'name' : 'test', 'description' : 'test'}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

        #do poprawy
    # def test_Form_is_valid(self):
    #     ingredient = Ingredient(name = "testIngredient", price = 2.43)
    #     current_user = User(username='test', first_name='test', last_name='test')
    #     new_recipe = Recipe(add_date=datetime.now(), author=current_user)
    #     form_data = {'name': 'testName', 'description': 'testDescript', 'ingredients' : ingredient}
    #     form = RecipeForm(instance=new_recipe, data=form_data)
    #     self.assertTrue(form.is_valid())

    #do zrobienia
# class UnitCalculatorTest(ut.TestCase):
