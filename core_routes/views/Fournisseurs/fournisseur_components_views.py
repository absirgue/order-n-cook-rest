from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.fournisseur_serializers import *
from rest_framework.views import APIView

"""
This file holds all view classes related to the Produit model. 
"""
class ProduitListAPIView(APIView):
    """
    Get a list of or create an Produit.
    """
    def get(self, request, format=None):
        fournisseurs = Produit.objects.all()
        fournisseur_serializer = ProduitSerializer(fournisseurs, many=True)
        
        return Response(fournisseur_serializer.data)

    def post(self, request, format=None):
        serializer = ProduitSerializer(data=request.data)
        if serializer.is_valid():
            produit = serializer.save()
            ProduitPriceTracker.objects.create(produit=produit,kilogramme_price=get_kilogramme_price(produit.ingredient,produit.unit,produit.quantity,produit.price))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProduitDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Produit item.
    """
    def get_object(self, pk):
        try:
            return Produit.objects.get(pk=pk)
        except Produit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        produit_object = self.get_object(pk)
        produit_serializer = ProduitDetailSerializer(produit_object)
        return Response(produit_serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProduitDetailSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            if "price" in request.data:
                ProduitPriceTracker.objects.create(produit=snippet,kilogramme_price=get_kilogramme_price(snippet.ingredient,snippet.unit,snippet.quantity,snippet.price))
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    