"""Unit tests for the Education Record model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from core_routes.models import Labels
from datetime import date
from django.db.utils import IntegrityError

class LabelsModelTestCase(TestCase):
    """Unit tests for the Label model."""

    fixtures = [
        'core_routes/test/fixtures/default_ingredient.json',
        'core_routes/test/fixtures/default_allergenes.json',
        'core_routes/test/fixtures/default_labels.json',
    ]

    def setUp(self):
        self.label = Labels.objects.get(id = 1)

    def test_valid_label_record(self):
        self._assert_label_is_valid()

    def test_a_label_name_can_be_75_characters(self):
        self.label.name = 'a'*75
        self._assert_label_is_valid()
    
    def test_a_label_name_can_not_be_more_than_75_characters(self):
        self.label.name = 'a'*76
        self._assert_label_is_invalid()
    
    def _assert_label_is_valid(self):
        try:
            self.label.full_clean()
        except (ValidationError):
            self.fail('Label should be valid')

    def _assert_label_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.label.full_clean()