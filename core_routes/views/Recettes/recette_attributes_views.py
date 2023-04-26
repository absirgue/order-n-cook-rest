from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *



class RecetteTasteListView(APIView):
    def get(self, request, format=None):
        recettes = RecetteTaste.objects.all()
        serializer = RecetteTasteSerializer(recettes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecetteTasteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
This file holds all view classes related to the RecetteGenres, RecetteInspirations,
RecetteTastes and RecetteCategories models. 
"""
class RecetteGenreDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecetteGenres item.
    """
    def get_object(self, pk):
        try:
            return RecetteGenre.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteGenreSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteGenreSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self,request, format=None):
        serializer = RecetteGenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecetteGenreListView(APIView):
    def get(self, request, format=None):
        recettes = RecetteGenre.objects.all()
        serializer = RecetteGenreSerializer(recettes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecetteGenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RecetteCategoryListView(APIView):
    def get(self, request, format=None):
        recettes = RecetteCategory.objects.all()
        serializer = RecetteCategorySerializer(recettes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecetteCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class RecetteCategoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecetteCategories item.
    """
    def get_object(self, pk):
        try:
            return RecetteCategory.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteCategorySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteCategorySerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self,request, format=None):
        serializer = RecetteCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecetteTasteDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecetteTastes item.
    """
    def get_object(self, pk):
        try:
            return RecetteTaste.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteTasteSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteTasteSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self,request, format=None):
        serializer = RecetteTasteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
