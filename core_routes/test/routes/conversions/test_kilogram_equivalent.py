from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from core_routes.models import Ingredients,Conversions


class KilogramEquivalentAPIViewTest(TestCase):
    """Tests of the routes associated with the conversion equivalence view."""
    
    fixtures = ['core_routes/test/fixtures/other_ingredient.json','core_routes/test/fixtures/default_conversions.json','core_routes/test/fixtures/default_labels.json','core_routes/test/fixtures/default_allergenes.json']

    def setUp(self):
        self.ingredient = Ingredients.objects.get(id=2)
        self.conversion = Conversions.objects.get(id=1)
        self.url = reverse('kilogram_equivalent')

    def test_conversion_url(self):
        self.assertEqual(self.url, f'/api/kilogram_equivalent/')
    
    def test_can_get_conversion_rate_from_ingredient_default_unit_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':self.ingredient.unit,'quantity':2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],round(Decimal(0.1),1))
        self.assertEqual(response.data['equivalence'],0.2)
        self.assertEqual(response.data['unit_of_equivalence'],'kilogramme')
    
    def test_can_get_conversion_rate_from_kilogramme_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':"kilogramme",'quantity':2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],1)
        self.assertEqual(response.data['equivalence'],2)
        self.assertEqual(response.data['unit_of_equivalence'],'kilogramme')
    
    def test_can_get_conversion_rate_from_conversion_record_to_kilogramme(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':self.conversion.unit,'quantity':2}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['conversion_rate'],round(Decimal(self.conversion.conversion_to_kilo),4))
        self.assertEqual(response.data['equivalence'],1)
        self.assertEqual(response.data['unit_of_equivalence'],'gramme')
    
    def test_can_get_conversion_rate_for_inexisting_unit_fails_graciously(self):
        response = self.client.get(self.url,
    {'ingredient_id': self.ingredient.id,'unit':"IDontExist",'quantity':2}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_can_get_conversion_rate_for_inexisting_ingredient_fails_graciously(self):
        response = self.client.get(self.url,
    {'ingredient_id': 3,'unit':"kilogramme",'quantity':2}
        )
        self.assertEqual(response.status_code, 400)