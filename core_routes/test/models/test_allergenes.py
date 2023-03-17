"""Unit tests for the Education Record model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from core_routes.models import Allergenes
from datetime import date
from django.db.utils import IntegrityError

class AllergenesModelTestCase(TestCase):
    """Unit tests for the Allergene model."""

    fixtures = [
        'core_routes/test/fixtures/default_ingredient.json',
        'core_routes/test/fixtures/default_allergenes.json',
        'core_routes/test/fixtures/default_labels.json',
    ]

    def setUp(self):
        self.allergene = Allergenes.objects.get(id = 1)

    def test_valid_allergene_record(self):
        self._assert_allergene_is_valid()

    def test_an_allerge_name_can_be_75_characters(self):
        self.allergene.name = 'a'*75
        self._assert_allergene_is_valid()
    
    def test_an_allerge_name_can_not_be_more_than_75_characters(self):
        self.allergene.name = 'a'*76
        self._assert_allergene_is_invalid()
    
    def _assert_allergene_is_valid(self):
        try:
            self.allergene.full_clean()
        except (ValidationError):
            self.fail('Allergenes should be valid')

    def _assert_allergene_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.allergene.full_clean()