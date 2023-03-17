from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Allergenes
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class AllergeneDetailAPIViewTest(TestCase):
    """Tests of the routes associated with an allergene's detailed view."""
    
    fixtures = ['core_routes/test/fixtures/default_allergenes.json']

    def setUp(self):
        self.post_data = {
            'name': 'testAllergene',
        }
        self.allergene = Allergenes.objects.get(id=1)
        self.url = reverse('allergene_detail', kwargs={'pk': self.allergene.id})

    def test_allergene_detail_url(self):
        self.assertEqual(self.url, f'/api/allergenes/{self.allergene.id}/')
    
    def test_can_get_an_allergene_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'],self.allergene.id)
        self.assertEqual(response.data['name'],self.allergene.name)

    def test_getting_invalid_allergene_fails_gracisouly(self):
        url = self._get_url_for_allergene_id(3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_delete_an_allergene(self):
        url = self._get_url_for_allergene_id(2)
        response = self.client.delete(url)
        with self.assertRaises(Allergenes.DoesNotExist): 
            Allergenes.objects.get(id=2)
    
    def test_deleting_invalid_allergene_fails_gracisouly(self):
        url = self._get_url_for_allergene_id(3)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_update_an_allergene_name(self):
        self.assertEqual(self.allergene.name,"Lactose")
        response = self.client.put(self.url,{'name':'Noix'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Allergenes.objects.get(id=1).name,"Noix")
    
    def test_updating_invalid_allergene_fails_gracisouly(self):
        self.assertEqual(self.allergene.name,"Lactose")
        response = self.client.put(self._get_url_for_allergene_id(3),{'name':"testerName"}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_posting_to_allergene_detail_is_not_allowed(self):
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,405)

    def _get_url_for_allergene_id(self,itemId):
        return reverse('allergene_detail', kwargs={'pk': itemId})