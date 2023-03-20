from django.urls import path
from core_routes import views

urlpatterns = [
    path('allergenes/<int:pk>/', views.AllergenesDetailAPIView.as_view(),name='allergene_detail'),
    path('labels/<int:pk>/', views.LabelsDetailAPIView.as_view(),name='label_detail'),
    path('allergenes/',views.AllergenesListAPIView.as_view(),name='allergene_list'),
    path('labels/',views.LabelsListAPIView.as_view(),name='label_list'),    
    path('ingredients/<int:pk>/', views.IngredientsDetailAPIView.as_view(),name="ingredient_detail"),
    path('ingredients/', views.IngredientsListAPIView.as_view(),name='ingredient_list'),
    path('remove_label_from_ingredient/<int:ingredientId>/<int:labelId>',views.LabelIngredientDelete.as_view()),
    path('remove_allergene_from_ingredient/<int:ingredientId>/<int:allergeneId>',views.AllergeneIngredientDelete.as_view()),
    path('conversion_rate/',views.ConversionIngredient.as_view(),name='conversion_rate'),
    path('kilogram_equivalent/',views.UnitEquivalence.as_view(),name='kilogram_equivalent'),
    path('ingredient_units/<int:ingredientId>/',views.IngredientUnits.as_view(),name='ingredient_unit')
]