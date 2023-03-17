"""Unit tests for the Education Record model."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from core_routes.models import Ingredients,Labels,Allergenes
from datetime import date
from django.db.utils import IntegrityError

class IngredientsModelTestCase(TestCase):
    """Unit tests for the Ingredient model."""

    fixtures = [
        'core_routes/test/fixtures/default_ingredient.json',
        'core_routes/test/fixtures/default_allergenes.json',
        'core_routes/test/fixtures/default_labels.json',
        'core_routes/test/fixtures/other_ingredient.json',
    ]

    def setUp(self):
        self.ingredient = Ingredients.objects.get(id = 1)

    def test_valid_ingredient_record(self):
        self._assert_ingredient_is_valid()

    def test_an_ingredient_can_have_no_label(self):
        self.ingredient.labels.set([])
        self._assert_ingredient_is_valid()
    
    def test_an_ingredient_can_have_no_allergene(self):
        self.ingredient.allergenes.set([])
        self._assert_ingredient_is_valid()
    
    def test_an_ingredient_can_have_multiple_labels(self):
        self.ingredient.labels.set([1,2])
        self._assert_ingredient_is_valid()
    
    def test_an_ingredient_can_have_multiple_allergenes(self):
        self.ingredient.allergenes.set([1,2])
        self._assert_ingredient_is_valid()
    
    def test_ingredient_description_can_not_be_empty(self):
        self.ingredient.description = None
        self._assert_ingredient_is_invalid()
    
    def test_ingredient_description_can_be_500_characters(self):
        self.ingredient.description = 500*'a'
        self._assert_ingredient_is_valid()
    
    def test_ingredient_name_can_not_be_empty(self):
        self.ingredient.name = None
        self._assert_ingredient_is_invalid()
    
    def test_ingredient_name_can_be_120_characters(self):
        self.ingredient.name = 120 *'a'
        self._assert_ingredient_is_valid()
    
    def test_ingredient_name_can_not_be_121_characters(self):
        self.ingredient.name = 121 *'a'
        self._assert_ingredient_is_invalid()
    
    def test_ingredient_illustration_can_be_empty(self):
        self.ingredient.illustration = None
        self._assert_ingredient_is_valid()
    
    def test_ingredient_illustration_can_be_a_string(self):
        self.ingredient.illustration = "image/test/IAmAPicture.png"
        self._assert_ingredient_is_valid()
    
    def test_ingredient_unit_defaults_to_kilogramme(self):
        ingredient = Ingredients.objects.create(name="Test",description="A description",illustration="image.jpeg")
        self.assertEqual(ingredient.unit, "kilogramme")
    
    def test_ingredient_conversion_to_kilo_defaults_to_kilogramme(self):
        ingredient = Ingredients.objects.create(name="Test",description="A description",illustration="image.jpeg")
        self.assertEqual(ingredient.conversion_to_kilo, 1.0)
    
    def test_deleting_a_label_does_not_impact_ingredient(self):
        ingredient = Ingredients.objects.get(id=2)
        label = Labels.objects.get(id=1)
        label.delete()
        ingredient.full_clean()
    
    def test_deleting_an_allergene_does_not_impact_ingredient(self):
        ingredient = Ingredients.objects.get(id=2)
        allergene = Allergenes.objects.get(id=1)
        allergene.delete()
        ingredient.full_clean()
    
    def test_deleting_an_allergene_does_not_impact_ingredient_even_if_just_one_allergene(self):
        ingredient = Ingredients.objects.get(id=1)
        allergene = Allergenes.objects.get(id=1)
        allergene.delete()
        self._assert_ingredient_is_valid()
    
    def test_deleting_a_label_does_not_impact_ingredient_even_if_just_one_allergene(self):
        ingredient = Ingredients.objects.get(id=1)
        label = Labels.objects.get(id=1)
        label.delete()
        self._assert_ingredient_is_valid()

    def test_conversion_to_kilo_can_be_12_digits(self):
        self.ingredient.conversion_to_kilo = round(Decimal(11111.1111110),7)
        self._assert_ingredient_is_valid()
    
    def test_conversion_to_kilo_can_not_be_13_digits(self):
        self.ingredient.conversion_to_kilo = 111111.111111
        self._assert_ingredient_is_invalid()
    
    def test_conversion_to_kilo_can_not_be_8_decimal_digits(self):
        self.ingredient.conversion_to_kilo = 111111.11113111
        self._assert_ingredient_is_invalid()
    
    def test_conversion_to_kilo_can_be_7_decimal_digits(self):
        self.ingredient.conversion_to_kilo = round(Decimal(11111.1111110),7)
        self._assert_ingredient_is_valid()
    
    def test_conversion_to_kilo_can_be_0(self):
        self.ingredient.conversion_to_kilo = 0
        self._assert_ingredient_is_valid()
    
    def test_conversion_to_kilo_can_not_be_negative(self):
        self.ingredient.conversion_to_kilo = -1
        self._assert_ingredient_is_invalid()
        
    def _assert_ingredient_is_valid(self):
        try:
            self.ingredient.full_clean()
        except (ValidationError):
            self.fail('Ingredient should be valid')

    def _assert_ingredient_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()