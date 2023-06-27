from django.urls import path
from core_routes.views.Ingredients.allergenes_and_labels_views import *
from core_routes.views.Ingredients.conversion_views import *
from core_routes.views.Ingredients.ingredient_views import *
from core_routes.views.Recettes.recette_attributes_views import *
from core_routes.views.Recettes.recettes_components import *
from core_routes.views.Recettes.recettes_views import *
from core_routes.views.Fournisseurs.fournisseur_views import *
from core_routes.views.Fournisseurs.fournisseur_components_views import *
from core_routes.views.Commandes.commande_views import *
from core_routes.views.Commandes.commande_operations import *

urlpatterns = [
    path('allergenes/<int:pk>/', AllergenesDetailAPIView.as_view(),name='allergene_detail'),
    path('labels/<int:pk>/', LabelsDetailAPIView.as_view(),name='label_detail'),
    path('allergenes/',AllergenesListAPIView.as_view(),name='allergene_list'),
    path('labels/',LabelsListAPIView.as_view(),name='label_list'),    
    path('ingredients/<int:pk>/', IngredientsDetailAPIView.as_view(),name="ingredient_detail"),
    path('ingredients/', IngredientsListAPIView.as_view(),name='ingredient_list'),
    path('ingredient_categories/', IngredientCategories.as_view(),name='ingredient_category'),
    path('ingredient_sous_categories/', IngredientSousCategories.as_view(),name='ingredient_sous_category'),
    path('remove_label_from_ingredient/<int:ingredientId>/<int:labelId>',LabelIngredientDelete.as_view()),
    path('remove_allergene_from_ingredient/<int:ingredientId>/<int:allergeneId>',AllergeneIngredientDelete.as_view()),
    path('conversion_rate/',ConversionIngredient.as_view(),name='conversion_rate'),
    path('kilogram_equivalent/',UnitEquivalence.as_view(),name='kilogram_equivalent'),
    path('all_ingredient_and_units/',IngredientsUnitsListView.as_view(),name='ingredients_unit'),
    path('all_ingredient_units_and_labels/',IngredientUnitsLabelsListView.as_view(),name='ingredients_unit_labels'),
    path('ingredient_units/<int:ingredientId>/',IngredientUnits.as_view(),name='ingredient_unit'),
    path('recettes/',RecetteListAPIView.as_view(),name='recettes_list'),
    path('recettes/<int:pk>/',RecetteDetailAPIView.as_view(),name='recettes_detail'),
    path('recette_ingredients/<int:pk>/',RecetteIngredientsDetailAPIView.as_view(),name='recette_ingredients_pk'),
    path('recette_ingredients/',RecetteIngredientsDetailAPIView.as_view(),name='recette_ingredients'),
    path('recette_genres/',RecetteGenreListView.as_view(),name='recette_genres'),
    path('recette_genre/<int:pk>/',RecetteGenreDetailAPIView.as_view(),name='recette_genres_pk'),
    path('recette_taste/<int:pk>/',RecetteTasteDetailAPIView.as_view(),name='recette_taste_pk'),
    path('recette_tastes/',RecetteTasteListView.as_view(),name='recette_taste'),
    path('recette_category/<int:pk>/',RecetteCategoryDetailAPIView.as_view(),name='recette_category_pk'),
    path('recette_categories/',RecetteCategoryListView.as_view(),name='recette_category_pk'),
    path('sous_recette/<int:pk>/',SousRecettesDetailAPIView.as_view(),name='sous_recette_pk'),
    path('sous_recette/',SousRecettesDetailAPIView.as_view(),name='sous_recette'),
    path('recette_progression/<int:pk>/',RecetteProgressionDetailAPIView.as_view(),name='recette_progression_pk'),
    path('recette_progression/',RecetteProgressionDetailAPIView.as_view(),name='recette_progression'),
    path('sous_recette_options/<int:recette_id>/',SousRecetteListView.as_view(),name='sous_recette_options'),
    path('increment_progression_rank/<int:progression_element_id>/',IncrementProgressionElementRank.as_view(),name='increment_rank'),
    path('decerement_progression_rank/<int:progression_element_id>/',DecrementProgressionElementRank.as_view(),name='decrement_rank'),
    path('recette_section/<int:pk>/',RecetteSectionDetailAPIView.as_view(),name='recette_section_pk'),
    path('recette_section/',RecetteSectionDetailAPIView.as_view(),name='recette_section'),
    path('duplicate_recette/<int:recette_id>/',DuplicateRecette.as_view(),name='duplicate_recette'),
    path('fournisseurs/', ForunisseurListAPIView.as_view(),name='fournisseur_list'),
    path('fournisseur_categories/', FournisseurCategoryView.as_view(),name='fournisseur_category'),
    path('fournisseur_specialties/', FournisseurSpecialityView.as_view(),name='fournisseur_specialty'),
    path('fournisseurs/<int:pk>/',FournisseurDetailAPIView.as_view(),name='fournisseurs_detail'),
    path('produits/',ProduitListAPIView.as_view(),name='produit_list'),
    path('produits/<int:pk>/',ProduitDetailAPIView.as_view(),name='produit_list'),
    path('ingredient/produits/<int:ingredient_id>',ProduitsForIngredientsView.as_view(),name='produits_for_ingredient'),
    path('commandes/',CommandeListAPIView.as_view(),name='commandes_list'),
    path('commandes/<int:pk>/',CommandeDetailAPIView.as_view(),name='commande_detail'),
    path('record_delivery/<int:pk>/',RecordDeliveryAPIView.as_view(),name='record_delivery'),
    path('create_avoir/<int:pk>/',CreateAvoirAPIView.as_view(),name='create_avoir'),
    path('receive_avoir/<int:commande_id>/',ReceiveAvoirAPIView.as_view(),name='receive_avoir'),
    path('fournisseur/order_data/<int:fournisseur_id>/',FournisseurMinimalDetailView.as_view(),name='fournisseur_detail_for_orders')
]