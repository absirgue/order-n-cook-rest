from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Labels
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class AllergeneListAPIViewTest(TestCase):
    """Tests of the routes associated with an allergene's detailed view."""
    
    fixtures = ['core_routes/test/fixtures/default_labels.json']

    def setUp(self):
        self.post_data = {
            'name': 'testLabel',
        }
        self.label = Labels.objects.get(id=1)
        self.other_label = Labels.objects.get(id=2)
        self.url = reverse('label_list')

    def test_allergene_list_url(self):
        self.assertEqual(self.url, f'/api/labels/')
    
    def test_can_get_an_allergene_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1]['id'],self.other_label.id)
        self.assertEqual(response.data[1]['name'],self.other_label.name)
        self.assertEqual(response.data[0]['id'],self.label.id)
        self.assertEqual(response.data[0]['name'],self.label.name)

    def test_getting_list_when_no_allergene_works(self):
        self.label.delete()
        self.other_label.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),0)
    
    def test_posting_an_allergene_works(self):
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Labels.objects.get(name='testLabel'))
    
    def test_posting_allergene_with_invalid_data_fails_graciously(self):
        del self.post_data['name']
        response = self.client.post(self.url,self.post_data)
        self.assertEqual(response.status_code, 400)
