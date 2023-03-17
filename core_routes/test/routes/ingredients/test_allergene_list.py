from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Allergenes
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class AllergeneListAPIViewTest(TestCase):
    """Tests of the routes associated with an allergene's detailed view."""
    
    fixtures = ['core_routes/test/fixtures/default_allergenes.json']

    def setUp(self):
        self.post_data = {
            'name': 'testAllergene',
        }
        self.allergene = Allergenes.objects.get(id=1)
        self.other_allergene = Allergenes.objects.get(id=2)
        self.url = reverse('allergene_list')

    def test_allergene_list_url(self):
        self.assertEqual(self.url, f'/api/allergenes/')
    
    def test_can_get_an_allergene_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1]['id'],self.other_allergene.id)
        self.assertEqual(response.data[1]['name'],self.other_allergene.name)
        self.assertEqual(response.data[0]['id'],self.allergene.id)
        self.assertEqual(response.data[0]['name'],self.allergene.name)

    def test_getting_list_when_no_allergene_works(self):
        self.allergene.delete()
        self.other_allergene.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),0)
    
    def test_posting_an_allergene_works(self):
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Allergenes.objects.get(name='testAllergene'))
    
    def test_posting_allergene_with_invalid_data_fails_graciously(self):
        del self.post_data['name']
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 400)
