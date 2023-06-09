from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *
from core_routes.serializers import ProduitForIngredientSerializer

"""
This file holds all view classes related to the Ingredients model. 
"""
class IngredientsListAPIView(APIView):
    """
    Get a list of or create an Ingredient.
    """
    def get(self, request, format=None):
        ingredients = Ingredients.objects.all()
        ingredient_serializer = IngredientsListSerializer(ingredients, many=True)
        
        return Response(ingredient_serializer.data)

    def post(self, request, format=None):
        serializer = IngredientsSerializer(data=request.data)
        if serializer.is_valid():
            if not Ingredients.objects.filter(name=request.data["name"]).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IngredientsDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet an Ingredients item.
    """
    def get_object(self, pk):
        try:
            return Ingredients.objects.get(pk=pk)
        except Ingredients.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = IngredientsDetailSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = IngredientsSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IngredientCategories(APIView):
    """
    Get a list of or create an Ingredient Category.
    """
    def get(self, request, format=None):
        ingredients = IngredientsCategories.objects.all()
        ingredient_serializer = IngredientsCategoriesSerializer(ingredients, many=True)
        
        return Response(ingredient_serializer.data)

    def post(self, request, format=None):
        serializer = IngredientsCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IngredientSousCategories(APIView):
    """
    Get a list of or create an Ingredient Sous Category.
    """
    def get(self, request, format=None):
        ingredients = IngredientsSubCategories.objects.all()
        ingredient_serializer = IngredientsSubCategoriesSerializer(ingredients, many=True)
        
        return Response(ingredient_serializer.data)

    def post(self, request, format=None):
        serializer = IngredientsSubCategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProduitsForIngredientsView(APIView):
     def get(self, request,ingredient_id, format=None):
        produits_for_ingredient = Produit.objects.filter(ingredient=ingredient_id)
        ingredient_serializer = ProduitForIngredientSerializer(produits_for_ingredient, many=True)
        
        return Response(ingredient_serializer.data)
