"""Unit tests for the Education Record model."""
from core_routes.helpers.helper_functions import get_upstream_depencies,get_downstream_depencies,get_dependencies
from django.test import TestCase
from core_routes.models import SousRecette

class DependencyAlgorithmTestCase(TestCase):
    """Unit tests for the dependency identification algorithm model."""

    fixtures = [
        'core_routes/test/fixtures/dependency_recette.json',
        'core_routes/test/fixtures/dependency_sous_recette.json',
    ]

    def test_upstream_dependency_retrieved_as_planned(self):
        upstream_dependencies = get_upstream_depencies(1)
        self.assertEqual(upstream_dependencies,{1,6,7,8})     

    def test_downstream_dependency_retrieved_as_planned(self):
        downstream_depencies = get_downstream_depencies(1)
        self.assertEqual(downstream_depencies,{1,2,3,4,5,9})

    def test_all_dependency_retrieved_as_planned(self):
        dependencies = get_dependencies(1)
        self.assertEqual(dependencies,{1,2,3,4,5,6,7,8,9})

    def test_successful_when_no_upstream(self):
        upstream_sous_recette_objects = [5,6,7]
        for id in upstream_sous_recette_objects:
            SousRecette.objects.get(id=id).delete()
        dependencies = get_dependencies(1)
        self.assertEqual(dependencies,{1,2,3,4,5,9})

    def test_successful_when_no_downstream(self):
        downstream_sous_recette_objects = [1,2,3,4,8]
        for id in downstream_sous_recette_objects:
            SousRecette.objects.get(id=id).delete()
        dependencies = get_dependencies(1)
        self.assertEqual(dependencies,{1,6,7,8})