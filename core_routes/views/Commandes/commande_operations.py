from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.commande_serializer import *
from rest_framework.views import APIView
import random
import string
import decimal


class RecordDeliveryAPIView(APIView):
    """
   Record the delivery of a Commande.
    """
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        commande = self.get_object(pk)
        if commande.status =="WAITING_DELIVERY":
            serializer = BonLivraisonSerializer(data=request.data)
            if serializer.is_valid():
                bl = serializer.save()
                commande.bon_livraison = bl
                commande.status = "WAITING_INVOICE"
                commande.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)
       


class CreateAvoirAPIView(APIView):
    """
    Record an avoir for a Commande.
    """
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        commande = self.get_object(pk)
        if commande.status =="WAITING_INVOICE":
            items = request.data["items"]
            avoir_items = []
            for item in items:
                avoir_item_serializer = AvoirItemSerializer(data=item)
                if avoir_item_serializer.is_valid():
                    avoir_item = avoir_item_serializer.save()
                    avoir_items.append(avoir_item)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            found_unique_avoir_nb = False
            avoir_unique_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            while not found_unique_avoir_nb:
                if Avoir.objects.filter(number=avoir_unique_number).exists():
                    avoir_unique_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                else:
                    found_unique_avoir_nb = True
            total_amount_ht = 0
            ids_of_items = []
            for item in avoir_items:
                total_amount_ht += float(item.item.quantity * item.item.unit_price)
                ids_of_items.append(item.id)
            avoir_serializer = AvoirSerializer(data={"items":ids_of_items,"number":avoir_unique_number,"total_amount_ht":total_amount_ht})
            if avoir_serializer.is_valid():
                avoir = avoir_serializer.save()
                commande.avoir = avoir
                commande.status = "WAITING_AVOIR"
                commande.concerned_with_avoir = True
                commande.save()
                for avoir_item in avoir.items.all():
                    commande_item = avoir_item.item
                    commande_item.pending_avoir = True
                    commande_item.save()
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)
    
class ReceiveAvoirAPIView(APIView):
    """
    Receive an avoir for a Commande.
    """
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404
        
    def put(self, request, commande_id, format=None):
        commande = self.get_object(commande_id)
        if commande.status =="WAITING_AVOIR":
            items = request.data["items"]
            for item in items:
                avoir_item = AvoirItem.objects.get(id=item['id'])
                serializer = AvoirItemSerializer(avoir_item, data=item,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    if float(item['quantity_received']) > 0:
                        commande_item = avoir_item.item
                        commande_item.received_avoir = True
                        commande_item.pending_avoir = False
                        commande_item.quantity = decimal.Decimal(float(commande_item.quantity) - float(item['quantity_received']))
                        commande_item.save()
                else:
                    return Response({"message":"Computation was not finished"},status=status.HTTP_400_BAD_REQUEST)
            commande.status = "AVOIR_RECEIVED_WAITING_INVOICE"
            commande.save()
            avoir = commande.avoir
            avoir.date_received = date.today()
            total_amount = 0
            for item in avoir.items.all():
                total_amount += item.item.unit_price *item.quantity_received
            avoir.total_amount_ht = total_amount
            avoir.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)
