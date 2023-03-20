from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from core_routes.models import Ingredients,Conversions


class IngredientUnitAPIViewTest(TestCase):
    """Tests of the routes associated with an conversions view."""
    
    fixtures = ['core_routes/test/fixtures/other_ingredient.json','core_routes/test/fixtures/default_conversions.json','core_routes/test/fixtures/default_labels.json','core_routes/test/fixtures/default_allergenes.json','core_routes/test/fixtures/default_ingredient.json']

    def setUp(self):
        self.ingredient = Ingredients.objects.get(id=2)
        self.conversion = Conversions.objects.get(id=1)
        self.url = reverse('ingredient_unit', kwargs={'ingredientId': self.ingredient.id})

    def test_ingredient_unit_url(self):
        self.assertEqual(self.url, f'/api/ingredient_units/2/')
    
    def test_valid_return_for_ingredient_with_default_unit_and_conversion_record(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['units'][0]['unit'],'kilogramme')
        self.assertEqual(response.data['units'][0]['conversion_rate'],1)
        self.assertEqual(response.data['units'][1]['unit'],'cup')
        self.assertEqual(response.data['units'][1]['conversion_rate'],Decimal('0.1000000'))
        self.assertEqual(response.data['units'][2]['unit'],'millilittre')
        self.assertEqual(response.data['units'][2]['conversion_rate'],Decimal('0.0005000'))
    
    def test_valid_return_for_ingredient_with_default_unit_being_kilo(self):
        response = self.client.get(self._get_url_for_ingredient_id(1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['units'][0]['unit'],'kilogramme')
        self.assertEqual(response.data['units'][0]['conversion_rate'],1)
    
    def test_valid_return_for_ingredient_with_default_unit_not_being_kilo(self):
        ingredient = Ingredients.objects.get(id=1)
        ingredient.unit = 'scoop'
        ingredient.conversion_to_kilo = 3
        ingredient.save()
        response = self.client.get(self._get_url_for_ingredient_id(1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['units'][0]['unit'],'kilogramme')
        self.assertEqual(response.data['units'][0]['conversion_rate'],1)
        self.assertEqual(response.data['units'][1]['unit'],'scoop')
        self.assertEqual(response.data['units'][1]['conversion_rate'],Decimal('3.0000000'))
    
    def test_getting_units_of_inexisting_item_fails_graciously(self):
        response = self.client.get(self._get_url_for_ingredient_id(3))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], 'Ingredient does not exist.')

    def _get_url_for_ingredient_id(self,id):
        return reverse('ingredient_unit', kwargs={'ingredientId': id})