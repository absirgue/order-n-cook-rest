from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.commande_serializer import *
from rest_framework.views import APIView
import random
import string

"""
This file holds all view classes related to the Commande model. 
"""
class CommandeListAPIView(APIView):
    """
    Get a list of or create a Commande.
    """
    def get(self, request, format=None):
        commandes = Commande.objects.all()
        commande_serializer = CommandeListSerializer(commandes, many=True)
        
        return Response(commande_serializer.data)

    def post(self, request, format=None):
        found_unique_commande_nb = False
        commande_unique_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        while not found_unique_commande_nb:
            if Commande.objects.filter(commande_number=commande_unique_number).exists():
                commande_unique_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            else:
                found_unique_commande_nb = True
        items = request.data['items']
        del request.data['items']
        commande_items = []
        for commande_item in items:
                commande_item_serializer = CommandeItemAllFieldsSerializer(data=commande_item)
                if commande_item_serializer.is_valid():
                    commande_item_serializer.save()
                    commande_items.append(commande_item_serializer.data['id'])
                else:
                    return Response(commande_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        rest = request.data
        rest["commande_number"] = commande_unique_number
        rest["items"] = commande_items
        MONTH_3_LETTERS = ["Janv","Févr","Mars","Avr","Mai","Juin","Juill","Août","Sept","Oct","Nov","Déc"]
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        rest["month"] = MONTH_3_LETTERS[currentMonth-1] + " "+str(currentYear)[-2:]
        serializer = CommandeAllFieldsSerializer(data=rest)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommandeDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a Commande item.
    """
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        commande_object = self.get_object(pk)
        commande_serializer = CommandeDetailsSerializer(commande_object)
        return Response(commande_serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommandeDetailsSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CommandeDetailsSerializer(snippet).data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

