from .models import Account, Recipe, Ingredient, LiquidUnits, SolidUnits
from .utils import UnitCalculator
import unittest as ut

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
        form_data = {'name': 'test', 'description': 'test'}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())


class UnitCalculatorTest(ut.TestCase):
    def setUp(self) -> None:
        LiquidUnits.objects.create(unit="l", conversionFactorToMainUnit=1000)
        LiquidUnits.objects.create(unit="ml", conversionFactorToMainUnit=1)
        SolidUnits.objects.create(unit="kg", conversionFactorToMainUnit=1000)
        SolidUnits.objects.create(unit="g", conversionFactorToMainUnit=1)

    def tearDown(self) -> None:
        LiquidUnits.objects.get(unit="l").delete()
        LiquidUnits.objects.get(unit="ml").delete()
        SolidUnits.objects.get(unit="kg").delete()
        SolidUnits.objects.get(unit="g").delete()

    def test_calculator_should_raise_type_error_liquid_to_solid(self):
        fromUnit = LiquidUnits.objects.get(unit='l')
        toUnit = SolidUnits.objects.get(unit='kg')
        with self.assertRaises(TypeError) as raises:
            self.assertEqual(UnitCalculator.convert(fromUnit, toUnit, 10), 10)

    def test_calculator_should_raise_type_error_solid_to_liquid(self):
        toUnit = LiquidUnits.objects.get(unit='l')
        fromUnit = SolidUnits.objects.get(unit='kg')
        with self.assertRaises(TypeError) as raises:
            self.assertEqual(UnitCalculator.convert(fromUnit, toUnit, 10), 10)

    def test_calculator_should_pass_liquid_to_liquid_equal_unit(self):
        fromUnit = LiquidUnits.objects.get(unit='l')
        toUnit = LiquidUnits.objects.get(unit='l')
        self.assertEqual(UnitCalculator.convert(fromUnit, toUnit, 10), 10)

    def test_calculator_should_pass_solid_to_solid_equal_unit(self):
        fromUnit = SolidUnits.objects.get(unit='kg')
        toUnit = SolidUnits.objects.get(unit='kg')
        self.assertEqual(UnitCalculator.convert(fromUnit, toUnit, 10), 10)

    def test_calculator_should_pass_solid_to_solid_different_unit(self):
        fromUnit = SolidUnits.objects.get(unit='kg')
        toUnit = SolidUnits.objects.get(unit='g')
        self.assertEqual(UnitCalculator.convert(fromUnit, toUnit, 10), 10000)