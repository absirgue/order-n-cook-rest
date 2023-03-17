from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from core_routes.models import Labels
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile


class LabelDetailAPIViewTest(TestCase):
    """Tests of the routes associated with an label's detailed view."""
    
    fixtures = ['core_routes/test/fixtures/default_labels.json']

    def setUp(self):
        self.post_data = {
            'name': 'testLabel',
        }
        self.label = Labels.objects.get(id=1)
        self.url = reverse('label_detail', kwargs={'pk': self.label.id})

    def test_allergene_detail_url(self):
        self.assertEqual(self.url, f'/api/labels/{self.label.id}/')
    
    def test_can_get_a_label_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'],self.label.id)
        self.assertEqual(response.data['name'],self.label.name)

    def test_getting_invalid_label_fails_gracisouly(self):
        url = self._get_url_for_label_id(3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_delete_an_label(self):
        url = self._get_url_for_label_id(2)
        response = self.client.delete(url)
        with self.assertRaises(Labels.DoesNotExist): 
            Labels.objects.get(id=2)
    
    def test_deleting_invalid_label_fails_gracisouly(self):
        url = self._get_url_for_label_id(3)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'],"Not found.")
    
    def test_can_update_an_label_name(self):
        self.assertEqual(self.label.name,"AOC")
        response = self.client.put(self.url,{'name':'Bio'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.get(id=1).name,"Bio")
    
    def test_updating_invalid_label_fails_gracisouly(self):
        response = self.client.put(self._get_url_for_label_id(3),{'name':"testerName"}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_posting_to_label_detail_is_not_allowed(self):
        response = self.client.post(self.url,self.post_data, content_type='application/json')
        self.assertEqual(response.status_code,405)

    def _get_url_for_label_id(self,itemId):
        return reverse('label_detail', kwargs={'pk': itemId})