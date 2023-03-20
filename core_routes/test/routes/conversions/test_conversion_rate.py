from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from core_routes.models import Ingredients,Conversions


class ConversionAPIViewTest(TestCase):
    """Tests of the routes associated with an conversions view."""
    
    fixtures = ['core_routes/test/fixtures/other_ingredient.json','core_routes/test/fixtures/default_conversions.json','core_routes/test/fixtures/default_labels.json','core_routes/test/fixtures/default_allergenes.json']

    def setUp(self):
        self.post_data = {
            'ingredient': 2,
            'unit':'cup',
            'conversion_to_kilo':0.3
        }
        self.ingredient = Ingredients.objects.get(id=2)
        self.conversion = Conversions.objects.get(id=1)
        self.url = reverse('conversion_rate')

    def test_conversion_url(self):
        self.assertEqual(self.url, f'/api/conversion_rate/')
    
    def test_can_get_conversion_rate_from_ingredient_default_unit_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':self.ingredient.unit}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],round(Decimal(0.1),1))
    
    def test_can_get_conversion_rate_from_kilogramme_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':"kilogramme"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],round(Decimal(1),1))
    
    def test_can_get_conversion_rate_from_conversion_record_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':self.conversion.unit}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],round(Decimal(self.conversion.conversion_to_kilo),4))
    
    def test_can_get_conversion_rate_for_inexisting_unit_fails_graciously(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':"IDontExist"}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_can_get_conversion_rate_for_inexisting_ingredient_fails_graciously(self):
        response = self.client.get(self.url,
    {'ingredient_id': 3,'unit':"kilogramme"}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_can_create_a_conversion(self):
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertIsNotNone(Conversions.objects.filter(ingredient=Ingredients.objects.get(id=2),unit="cup"))
        self.assertEqual(Conversions.objects.get(ingredient=Ingredients.objects.get(id=2),unit="cup").conversion_to_kilo,Decimal('0.3000000'))
    
    def test_wrong_post_fails_graciously(self):
        del self.post_data['ingredient']
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,400)
    
    def test_can_not_create_conversion_for_inexistant_ingredient(self):
        self.post_data['ingredient'] = 1
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,400)