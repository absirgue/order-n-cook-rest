from django.urls import path
from core_routes import views

urlpatterns = [
    path('allergenes/<int:pk>/', views.AllergenesDetailAPIView.as_view()),
    path('labels/<int:pk>/', views.LabelsDetailAPIView.as_view()),
    path('allergenes/',views.AllergenesListAPIView.as_view()),
    path('labels/',views.LabelsListAPIView.as_view()),    
    path('ingredients/<int:pk>/', views.IngredientsDetailAPIView.as_view(),name="ingredient_detail"),
    path('ingredients/', views.IngredientsListAPIView.as_view()),
    path('remove_label_from_ingredient/<int:ingredientId>/<int:labelId>',views.LabelIngredientDelete.as_view()),
    path('remove_allergene_from_ingredient/<int:ingredientId>/<int:allergeneId>',views.AllergeneIngredientDelete.as_view()),
    path('conversion_rate/',views.ConversionIngredient.as_view()),
    path('kilogram_equivalent/',views.UnitEquivalence.as_view()),
    path('ingredient_units/<int:ingredientId>/',views.IngredientUnits.as_view())
]