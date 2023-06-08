from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

"""
This file holds all view classes related to the conversion of a given quantity of 
ingredient between two units.
"""
class ConversionIngredient(APIView):
    """
    Get, create, update, or delete the conversion rate for an item to an unit to kilogramme.
    """
    def get(self,request, format=None):
        ingredientId = request.GET.get('ingredient_id',None)
        unit = request.GET.get('unit',None)
        if not (ingredientId and unit):
            # Make error message more specific
            return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)

        conversion_rate = get_conversion_rate(ingredientId=ingredientId, unit=unit)
        if conversion_rate:
            return Response({'conversion_rate':conversion_rate},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Pas de conversion en kilorgamme trouvée.'},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = ConversionsSerializer(data=request.data)
        if serializer.is_valid():
            if not Conversions.objects.filter(ingredient=request.data["ingredient"],unit=request.data["unit"]).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        try:
            ingredientId = request.GET.get('ingredient_id',None)
            unit = request.GET.get('unit',None)
            if not (ingredientId and unit):
                # Make error message more specific
                return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)

            ingredient = Ingredients.objects.get(id=ingredientId)
            snippet = Conversions.objects.get(ingredient=ingredient,unit=unit)
            serializer = ConversionsSerializer(snippet, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        ingredientId = request.DELETE.get('ingredient_id',None)
        unit = request.DELETE.get('unit',None)
        if not (ingredientId and unit):
            # Make error message more specific
            return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)

        ingredient = Ingredients.objects.get(id=ingredientId)
        snippet = Conversions.objects.get(ingredient=ingredient,unit=unit)
        snippet.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

class UnitEquivalence(APIView):
    """
    Get the conversion to kilogramme from a quantity of a given item in a certain unit.
    """
    def get(self, request, format=None):
        ingredient_id = request.GET.get('ingredient_id',None)
        unit = request.GET.get('unit',None)
        quantity = float(request.GET.get('quantity',None))

        if not (ingredient_id and unit and quantity):
            # Make error message more specific
            return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)

        conversion_rate = get_conversion_rate(ingredientId=ingredient_id,unit=unit)
        if conversion_rate:
            equivalence = quantity * float(conversion_rate)
            unit = "kilogramme"
            if equivalence <0.1:
                equivalence = equivalence *1000
                unit = "gramme"
            return Response({'equivalence':equivalence,'conversion_rate':conversion_rate,'unit_of_equivalence':unit})
        else:
            return Response({'message':'Pas de conversion en kilorgamme trouvée.'},status=status.HTTP_400_BAD_REQUEST)

class IngredientsUnitsListView(APIView):
    """
    Get a list of the units available for an ingredient.
    """
    def get(self,request, format=None):
        ingredients = Ingredients.objects.all()
        ingredient_serializer = IngredientOnlyNameSerializer(ingredients, many=True)
        return Response(ingredient_serializer.data)
    
class IngredientsUnitsListView(APIView):
    """
    Get a list of the units available for an ingredient.
    """
    def get(self,request, format=None):
        ingredients = Ingredients.objects.all()
        ingredient_serializer = IngredientOnlyNameSerializer(ingredients, many=True)
        return Response(ingredient_serializer.data)
    
class IngredientUnits(APIView):
    """
    Get a list of the units available for an ingredient.
    """
    def get(self,request,ingredientId, format=None):
        if not (ingredientId):
            return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            ingredient = Ingredients.objects.get(id=ingredientId)
            print(ingredient)
            conversions = [{"unit":"kilogramme","conversion_rate":1}]
            if ingredient.unit != "kilogramme":
                conversions.append({"unit":ingredient.unit,"conversion_rate":ingredient.conversion_to_kilo})
            
            try:
                recorded_conversions = Conversions.objects.filter(ingredient=ingredient)
                for conversion in recorded_conversions:
                    conversions.append({"unit":conversion.unit,"conversion_rate":conversion.conversion_to_kilo})
                return Response({'units':conversions},status=status.HTTP_200_OK)
            except:
                return Response({'units':conversions},status=status.HTTP_200_OK)
        except:
            return Response({'message':'Ingredient does not exist.'},status=status.HTTP_404_NOT_FOUND)    


        

