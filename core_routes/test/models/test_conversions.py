"""Unit tests for the Education Record model."""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from core_routes.models import Allergenes,Conversions,Ingredients
from datetime import date
from django.db.utils import IntegrityError

class ConversionsModelTestCase(TestCase):
    """Unit tests for the Conversion model."""

    fixtures = [
        'core_routes/test/fixtures/default_ingredient.json',
        'core_routes/test/fixtures/default_allergenes.json',
        'core_routes/test/fixtures/default_labels.json',
    ]

    def setUp(self):
        self.conversion = Conversions.objects.create(id=1,ingredient = Ingredients.objects.get(id=1))

    def test_valid(self):
        self._assert_conversion_is_valid()

    def test_unit_defaults_to_kilogramme(self):
        self.assertEqual(self.conversion.unit,"kilogramme")
    
    def test_conversion_to_kilogramme_defaults_to_1(self):
        self.assertEqual(self.conversion.conversion_to_kilo,1.0)
    
    def test_conversion_can_not_have_invalid_ingredient(self):
        with self.assertRaises(ValueError): 
            self.conversion.ingredient = 3
    
    def test_conversion_is_deleted_when_item_is(self):
        Ingredients.objects.get(id=1).delete()
        with self.assertRaises(Conversions.DoesNotExist): 
            Conversions.objects.get(id=1)
        
    def test_ingredient_is_not_deleted_when_conversion_is(self):
        self.conversion.delete()
        self.assertEqual(Ingredients.objects.get(id=1).name,"Beurre")
    
    def test_unit_can_be_100_characters(self):
        self.conversion.unit = 'a'*100
        self._assert_conversion_is_valid()
    
    def test_unit_can_not_be_101_characters(self):
        self.conversion.unit = 'a'*101
        self._assert_conversion_is_invalid()
    
    def test_conversion_to_kilo_can_be_12_digits(self):
        self.conversion.conversion_to_kilo = round(Decimal(11111.1111110),7)
        self._assert_conversion_is_valid()
    
    def test_conversion_to_kilo_can_be_12_digits(self):
        self.conversion.conversion_to_kilo = round(Decimal(111111.111110),7)
        self._assert_conversion_is_valid()
    
    def test_conversion_to_kilo_can_not_be_13_digits(self):
        self.conversion.conversion_to_kilo = 111111.111111
        self._assert_conversion_is_invalid()
    
    def test_conversion_to_kilo_can_not_be_8_decimal_digits(self):
        self.conversion.conversion_to_kilo = 111111.11113111
        self._assert_conversion_is_invalid()
    
    def test_conversion_to_kilo_can_be_7_decimal_digits(self):
        self.conversion.conversion_to_kilo = round(Decimal(11111.1111110),7)
        self._assert_conversion_is_valid()
    
    def test_conversion_to_kilo_can_be_0(self):
        self.conversion.conversion_to_kilo = 0
        self._assert_conversion_is_valid()
    
    def test_conversion_to_kilo_can_not_be_negative(self):
        self.conversion.conversion_to_kilo = -1
        self._assert_conversion_is_invalid()
    
    def _assert_conversion_is_valid(self):
        try:
            self.conversion.full_clean()
        except (ValidationError):
            self.fail('Conversions should be valid')

    def _assert_conversion_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.conversion.full_clean()