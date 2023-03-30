from django.http import Http404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *


class RecettesListAPIView(APIView):
    """
    Get a list of or create a Recettes.
    """
    def get(self, request, format=None):
        allergenes = Recettes.objects.all()
        serializer = RecettesSerializer(allergenes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecettesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecettesDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Recettes item.
    """
    def get_object(self, pk):
        try:
            return Recettes.objects.get(pk=pk)
        except Recettes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        recette_object = self.get_object(pk)
        recette_data = RecettesSerializer(recette_object).data 
        ingredient_data = RecettesIngredients.objects.filter(recette = recette_object)
        if ingredient_data:
            recette_data["ingredients"] = RecettesIngredientsSerializer(ingredient_data).data
        progression_data = RecettesProgressionElements.objects.filter(recette = recette_object)
        if progression_data:
            recette_data["progression"] = RecettesProgressionElementsSerializer(ingredient_data).data
        sous_recettes_data = SousRecettes.objects.filter(recette = recette_object)
        if sous_recettes_data:
            sous_recette_list = []
            for sous_recette in sous_recettes_data:
                sous_recette_list.append({
                    "name":sous_recette.sous_recette.name,
                    "quantity": sous_recette.quantity,
                    "unit": sous_recette.unit,
                    "link": reverse('recettes_detail',kwargs={"pk":sous_recette.id})
                })
            recette_data["sous_recette"] = sous_recette_list

        print(recette_data)
        return Response(recette_data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecettesSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    