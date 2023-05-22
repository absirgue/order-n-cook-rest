from django.http import Http404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

"""
This file holds all view classes related to the Recette model.
"""
class RecetteListAPIView(APIView):
    """
    Get a list of or create a Recette.
    """
    def get(self, request, format=None):
        recettes = Recette.objects.all()
        serializer = RecetteListGetSerializer(recettes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecetteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecetteDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Recette item.
    """
    def get_object(self, pk):
        try:
            return Recette.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print("ACCESSED")
        recette_object = self.get_object(pk)
        recette_serializer = RecetteDetailGetSerializer(recette_object)
        return Response(recette_serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteSerializer(snippet, data=request.data,partial=True)
        print(request.data)
        if serializer.is_valid():
            print("VALID")
            serializer.save()
            return Response(RecetteDetailGetSerializer(snippet).data,status=status.HTTP_200_OK)
        else:
            print("GROS PB")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SousRecetteListView(APIView):
    def get(self, request, recette_id, format=None):
        recettes = Recette.objects.all()
        list_of_recettes = []
        for recette in recettes:
            if recette.id != recette_id and recette.unit and recette.quantity:
                list_of_recettes.append(recette)
        serialized_recettes = SousRecetteOptionSerializer(list_of_recettes,many=True)
        return Response(serialized_recettes.data)
    
class DuplicateRecette(APIView):
    def get(self, request, recette_id, format=None):
        # Check if caller is the author of the duplicated recette
        new_recette = Recette.objects.get(id = recette_id)
        new_recette.id = None
        new_recette.selected_for_menu = False
        new_recette.selected_for_next_menu = False
        new_recette.is_to_modify = True
        new_recette.name = new_recette.name + " (copie)"
        new_recette.save()
        for ingredient in RecetteIngredient.objects.filter(recette=recette_id):
            ingredient.id = None
            ingredient.recette = new_recette
            ingredient.save()
        for progression_element in RecetteProgressionElement.objects.filter(recette=recette_id):
            progression_element.id = None
            progression_element.recette = new_recette
            progression_element.save()
        for sous_recette in SousRecette.objects.filter(recette=recette_id):
            sous_recette.id = None
            sous_recette.recette = new_recette
            sous_recette.save()
        for section in RecetteSection.objects.filter(recette=recette_id):
            section.id = None
            section.recette = new_recette
            section.save()
        return Response({"id":new_recette.id},status=status.HTTP_201_CREATED)

    