from django.http import Http404
from rest_framework.generics import GenericAPIView,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

# Create your views here.
# 1. Getting a list of all ingredients ✅
# 2. Getting one ingredient with ID ✅
# 3. Adding an ingredient with all including allergenes and labels ✅
# 4. Adding a label to an ingredient ✅
# 5. Removing a label from an ingredient ✅
# 6. Adding an allergene to an ingredient ✅
# 7. Removing an allergene from an ingredient ✅
# 8. Create an allergene ✅
# 9. Create a label ✅
# 10. Delete a label ✅
# 11. Delete an allergene ✅
# 12. Update an allergene ✅
# 13. Update a label ✅
# 14. Update an ingredient (its own fields) ✅
# 15. Route to get weight in kilogramme (or return in gramme if small decimal) from a unit, returns a particular message if conversion not found ✅
# 16. Route to get all the units for an ingredient ✅
# 17. Build a route that gets the conversion rate ✅
# 18. Editing a conversion rate ✅
# 19. Adding a conversion rate ✅
# 20. Deleting a conversion rate ✅
# 21. Ensure conversion exists before enabling creation of recette ingredient ✅
# 22. Add GeneralConversions (gramme -> kilgoramme, ....) and getting a list of them for proposal on ingredient creation


class LabelsDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Labels item.
    """
    def get_object(self, pk):
        try:
            return Labels.objects.get(pk=pk)
        except Labels.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LabelsSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LabelsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllergenesDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet an Allergenes item.
    """
    def get_object(self, pk):
        try:
            return Allergenes.objects.get(pk=pk)
        except Allergenes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AllergenesSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AllergenesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllergenesListAPIView(APIView):
    """
    Get a list of or create an Allergene.
    """
    def get(self, request, format=None):
        allergenes = Allergenes.objects.all()
        serializer = AllergenesSerializer(allergenes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AllergenesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LabelsListAPIView(APIView):
    """
    Get a list of or create a Label.
    """
    def get(self, request, format=None):
        allergenes = Labels.objects.all()
        serializer = LabelsSerializer(allergenes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LabelsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IngredientsListAPIView(APIView):
    """
    Get a list of or create an Ingredient.
    """
    def get(self, request, format=None):
        ingredients = Ingredients.objects.all()
        ingredient_serializer = IngredientsGetSerializer(ingredients, many=True)
        return Response(ingredient_serializer.data)

    def post(self, request, format=None):
        serializer = IngredientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        serializer = IngredientsGetSerializer(snippet)
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

class LabelIngredientDelete(APIView):
    """
    Delete a Label from an Ingredient.
    """
    def get_object(self, pk):
        try:
            return Ingredients.objects.get(pk=pk)
        except Ingredients.DoesNotExist:
            raise Http404
        
    def delete(self,request,ingredientId, labelId, format=None):
        snippet = self.get_object(ingredientId)
        snippet.labels.remove(Labels.objects.get(id=labelId))
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllergeneIngredientDelete(APIView):
    """
    Delete an Allergene from an Ingredient.
    """
    def get_object(self, pk):
        try:
            return Ingredients.objects.get(pk=pk)
        except Ingredients.DoesNotExist:
            raise Http404
        
    def delete(self,request,ingredientId, allergeneId, format=None):
        snippet = self.get_object(ingredientId)
        snippet.allergenes.remove(Allergenes.objects.get(id=allergeneId))
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

class IngredientUnits(APIView):
    """
    Get a list of the units available for an ingredient.
    """
    def get(self,request,ingredientId, format=None):
        if not (ingredientId):
            return Response({'message':'Not enough data provided.'},status=status.HTTP_400_BAD_REQUEST)
        ingredient = Ingredients.objects.get(id=ingredientId)
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