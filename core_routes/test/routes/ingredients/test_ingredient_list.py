from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Ingredients,Allergenes,Labels
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class IngredientListAPIViewTest(TestCase):
    """Tests of the routes associated with an ingredient's list view."""
    
    fixtures = ['core_routes/test/fixtures/default_ingredient.json','core_routes/test/fixtures/other_ingredient.json','core_routes/test/fixtures/default_labels.json','core_routes/test/fixtures/default_allergenes.json',]

    def setUp(self):
        self.post_data = {
            'name': 'TestIngredient',
            'description': 'I am a test ingredient.',
            "labels": [
                1
            ],
            "allergenes": [
                1
            ],
            "conversion_to_kilo": 1.0,
            "unit": "kilogramme"
        }
        self.ingredient = Ingredients.objects.get(id=1)
        self.other_ingredient = Ingredients.objects.get(id=2)
        self.url = reverse('ingredient_list')

    def test_ingredient_list_url(self):
        self.assertEqual(self.url, f'/api/ingredients/')
    
    def test_can_get_an_ingredient_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1]['id'],self.other_ingredient.id)
        self.assertEqual(response.data[1]['name'],self.other_ingredient.name)
        self.assertEqual(response.data[1]['description'],self.other_ingredient.description)
        self.assertEqual(Decimal(response.data[1]['conversion_to_kilo']),self.other_ingredient.conversion_to_kilo)
        self.assertEqual(response.data[1]['unit'],self.other_ingredient.unit)
        self.assertEqual(response.data[0]['id'],self.ingredient.id)
        self.assertEqual(response.data[0]['name'],self.ingredient.name)
        self.assertEqual(response.data[0]['description'],self.ingredient.description)
        self.assertEqual(Decimal(response.data[0]['conversion_to_kilo']),self.ingredient.conversion_to_kilo)
        self.assertEqual(response.data[0]['unit'],self.ingredient.unit)

    def test_getting_list_when_no_ingredient_works(self):
        self.ingredient.delete()
        self.other_ingredient.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),0)
    
    def test_posting_an_ingredient_works(self):
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Ingredients.objects.get(name='TestIngredient'))
        self.assertEqual(Ingredients.objects.get(name='TestIngredient').description,'I am a test ingredient.')
    
    def test_posting_ingredient_with_invalid_data_fails_graciously(self):
        del self.post_data['name']
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 400)
