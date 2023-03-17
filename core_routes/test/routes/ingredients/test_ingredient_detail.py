from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Ingredients,Allergenes,Labels
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class IngredientDetailAPIViewTest(TestCase):
    """Tests of the routes associated with an ingredient's detailed view."""
    
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
        self.url = reverse('ingredient_detail', kwargs={'pk': self.ingredient.id})

    def test_ingredient_detail_url(self):
        self.assertEqual(self.url, f'/api/ingredients/{self.ingredient.id}/')
    
    def test_can_get_an_ingredient_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'],self.ingredient.id)
        self.assertEqual(response.data['name'],self.ingredient.name)
        self.assertEqual(response.data['description'],self.ingredient.description)
        self.assertEqual(Decimal(response.data['conversion_to_kilo']),self.ingredient.conversion_to_kilo)
        self.assertEqual(response.data['unit'],self.ingredient.unit)

    def test_getting_invalid_ingredient_fails_gracisouly(self):
        url = self._get_url_for_item_id(3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_delete_an_ingredient(self):
        url = self._get_url_for_item_id(2)
        response = self.client.delete(url)
        with self.assertRaises(Ingredients.DoesNotExist): 
            Ingredients.objects.get(id=2)
    
    def test_deleting_invalid_ingredient_fails_gracisouly(self):
        url = self._get_url_for_item_id(3)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_update_an_ingredient_name(self):
        self.assertEqual(self.ingredient.name,"Beurre")
        response = self.client.put(self.url,{'name':'newName'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredients.objects.get(id=1).name,"newName")
    
    def test_can_update_an_ingredient_description(self):
        self.assertEqual(self.ingredient.description,"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis nec eros in elit lobortis pretium. Pellentesque et est id ante posuere dignissim. Donec viverra gravida felis, vitae dictum augue tincidunt vel. Aenean placerat sem quis est ultrices, sit amet tempor turpis tempus. Pellentesque pulvinar, tellus eget luctus volutpat, ex metus euismod nisl, consectetur pellentesque elit ante in neque. Duis vulputate tortor a nibh vulputate lacinia. Sed aliquam tristique imperdiet.")
        response = self.client.put(self.url,{'description':'newDescription'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredients.objects.get(id=1).description,"newDescription")
    
    def test_can_update_an_ingredient_allergenes(self):
        response = self.client.put(self.url,{'allergenes':[1,2]}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['allergenes']),2)

    def test_updating_an_ingredient_with_inexistant_allergene_fails_graciously(self):
        response = self.client.put(self.url,{'allergenes':[1,3]}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_can_update_an_ingredient_labels(self):
        response = self.client.put(self.url,{'labels':[1,2]}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['labels']),2)
    
    def test_updating_an_ingredient_with_inexistant_label_fails_graciously(self):
        response = self.client.put(self.url,{'labels':[1,3]}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_can_update_an_ingredient_conversion_to_kilo(self):
        self.assertEqual(self.ingredient.conversion_to_kilo,1.0)
        response = self.client.put(self.url,{'conversion_to_kilo':4.0}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredients.objects.get(id=1).conversion_to_kilo,4.0)
    
    def test_can_update_an_ingredient_unit(self):
        self.assertEqual(self.ingredient.unit,"kilogramme")
        response = self.client.put(self.url,{'unit':"littre"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredients.objects.get(id=1).unit,"littre")
    
    def test_updating_invalid_ingredient_fails_gracisouly(self):
        self.assertEqual(self.ingredient.unit,"kilogramme")
        response = self.client.put(self._get_url_for_item_id(3),{'unit':"littre"}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_posting_to_ingredient_detail_is_not_allowed(self):
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,405)

    def _get_url_for_item_id(self,itemId):
        return reverse('ingredient_detail', kwargs={'pk': itemId})