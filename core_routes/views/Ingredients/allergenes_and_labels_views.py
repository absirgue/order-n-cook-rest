from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

"""
This file holds all view classes related to the Allergenes and Labels models. 
"""
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
  