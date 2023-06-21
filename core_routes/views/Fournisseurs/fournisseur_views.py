from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.fournisseur_serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

"""
This file holds all view classes related to the Fournisseur model. 
"""
class ForunisseurListAPIView(APIView):
    """
    Get a list of or create an Fournisseur.
    """
    def get(self, request, format=None):
        fournisseurs = Fournisseur.objects.all()
        fournisseur_serializer = FournisseurListSerializer(fournisseurs, many=True)
        
        return Response(fournisseur_serializer.data)

    def post(self, request, format=None):
        serializer = FournisseurAllFieldsSerializer(data=request.data)
        if serializer.is_valid():
            if not Fournisseur.objects.filter(name=request.data["name"]).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FournisseurCategoryView(APIView):
    """
    Get a list of or create a FournisseurCategory
    """
    def get(self, request, format=None):
        fournisseur_category = FournisseurCategory.objects.all()
        fournisseur_category_serializer = ForunisseurCategorySerializer(fournisseur_category, many=True)
        
        return Response(fournisseur_category_serializer.data)

    def post(self, request, format=None):
        serializer = ForunisseurCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FournisseurSpecialityView(APIView):
    """
    Get a list of or create a FournisseurSpecialty
    """
    def get(self, request, format=None):
        fournisseur_category = FournisseurSpecialty.objects.all()
        fournisseur_category_serializer = ForunisseurSpecialtySerializer(fournisseur_category, many=True)
        
        return Response(fournisseur_category_serializer.data)

    def post(self, request, format=None):
        serializer = ForunisseurSpecialtySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FournisseurDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Fournisseur item.
    """
    def get_object(self, pk):
        try:
            return Fournisseur.objects.get(pk=pk)
        except Fournisseur.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fournisseur_object = self.get_object(pk)
        fournisseur_serializer = FournisseurDetailSerializer(fournisseur_object)
        return Response(fournisseur_serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FournisseurAllFieldsSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(FournisseurDetailSerializer(snippet).data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FournisseurMinimalDetailView(APIView):
  
    def get_object(self, fournisseur_id):
        try:
            return Fournisseur.objects.get(pk=fournisseur_id)
        except Fournisseur.DoesNotExist:
            raise Http404

    def get(self, request, fournisseur_id, format=None):
        fournisseur_object = self.get_object(fournisseur_id)
        fournisseur_serializer = FournisseurOrderDetailSerializer(fournisseur_object)
        return Response(fournisseur_serializer.data)
