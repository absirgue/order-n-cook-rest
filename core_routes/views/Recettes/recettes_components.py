from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

class RecettesIngredientsDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return RecettesIngredients.objects.get(pk=pk)
        except Recettes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = GetRecettesIngredientsSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecettesIngredientsSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        serializer = CreateRecettesIngredientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SousRecettesDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return SousRecettes.objects.get(pk=pk)
        except Recettes.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SousRecettesSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        serializer = SousRecettesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class RecetteProgressionDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return RecettesProgressionElements.objects.get(pk=pk)
        except Recettes.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecettesProgressionElementsSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        serializer = RecettesProgressionElementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
