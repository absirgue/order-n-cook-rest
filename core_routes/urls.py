from django.urls import path
from core_routes.views.Ingredients.allergenes_and_labels_views import *
from core_routes.views.Ingredients.conversion_views import *
from core_routes.views.Ingredients.ingredient_views import *
from core_routes.views.Recettes.recette_attributes_views import *
from core_routes.views.Recettes.recettes_components import *
from core_routes.views.Recettes.recettes_views import *


urlpatterns = [
    path('allergenes/<int:pk>/', AllergenesDetailAPIView.as_view(),name='allergene_detail'),
    path('labels/<int:pk>/', LabelsDetailAPIView.as_view(),name='label_detail'),
    path('allergenes/',AllergenesListAPIView.as_view(),name='allergene_list'),
    path('labels/',LabelsListAPIView.as_view(),name='label_list'),    
    path('ingredients/<int:pk>/', IngredientsDetailAPIView.as_view(),name="ingredient_detail"),
    path('ingredients/', IngredientsListAPIView.as_view(),name='ingredient_list'),
    path('remove_label_from_ingredient/<int:ingredientId>/<int:labelId>',LabelIngredientDelete.as_view()),
    path('remove_allergene_from_ingredient/<int:ingredientId>/<int:allergeneId>',AllergeneIngredientDelete.as_view()),
    path('conversion_rate/',ConversionIngredient.as_view(),name='conversion_rate'),
    path('kilogram_equivalent/',UnitEquivalence.as_view(),name='kilogram_equivalent'),
    path('ingredient_units/<int:ingredientId>/',IngredientUnits.as_view(),name='ingredient_unit'),
    path('recettes/',RecettesListAPIView.as_view(),name='recettes_list'),
    path('recettes/<int:pk>/',RecettesDetailAPIView.as_view(),name='recettes_detail'),
    path('recette_ingredients/<int:pk>/',RecettesIngredientsDetailAPIView.as_view(),name='recette_ingredients_pk'),
    path('recette_ingredients/',RecettesIngredientsDetailAPIView.as_view(),name='recette_ingredients'),
    path('recette_genres/',RecettesGenresDetailAPIView.as_view(),name='recette_genres'),
    path('recette_genre/<int:pk>/',RecettesGenresDetailAPIView.as_view(),name='recette_genres_pk'),
    path('recette_inspiration/<int:pk>/',RecettesInspirationsDetailAPIView.as_view(),name='recette_inspiration_pk'),
    path('recette_inspirations/',RecettesInspirationsDetailAPIView.as_view(),name='recette_inspiration'),
    path('recette_taste/<int:pk>/',RecettesTastesDetailAPIView.as_view(),name='recette_taste_pk'),
    path('recette_tastes/',RecettesTastesDetailAPIView.as_view(),name='recette_taste'),
    path('recette_category/<int:pk>/',RecettesCategoriesDetailAPIView.as_view(),name='recette_category_pk'),
    path('recette_categories/',RecettesCategoriesDetailAPIView.as_view(),name='recette_category_pk'),
    path('sous_recette/<int:pk>/',SousRecettesDetailAPIView.as_view(),name='sous_recette_pk'),
    path('sous_recette/',SousRecettesDetailAPIView.as_view(),name='sous_recette'),
    path('recette_progression/<int:pk>/',RecetteProgressionDetailAPIView.as_view(),name='recette_progression_pk'),
    path('recette_progression/',RecetteProgressionDetailAPIView.as_view(),name='recette_progression'),
]