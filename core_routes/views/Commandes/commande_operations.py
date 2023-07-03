from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.commande_serializer import *
from core_routes.fournisseur_serializers import *
from rest_framework.views import APIView
import random
import string
import decimal
from core_routes.utils import render_to_pdf
from django.http import HttpResponse
from core_routes.textract import TextractWrapper
from rest_framework.parsers import FileUploadParser

DAYS_OF_THE_WEEK = ["Lundi","Mardi","Mercredi","Jeudi",'Vendredi',"Samedi","Dimanche"]
MONTHS = ["Janvier","Février","Mars","Avril",'Mai',"Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

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
                pdf_items = []
                for avoir_item in avoir.items.all():
                    commande_item = avoir_item.item
                    commande_item.pending_avoir = True
                    commande_item.save()
                    pdf_items.append({'quantity':str(round(avoir_item.quantity_demanded*avoir_item.item.unit_quantity, 2)),'unit':avoir_item.item.unit,'produit_name':avoir_item.item.produit.ingredient.name,'unit_price':f"{avoir_item.item.unit_price}%s"%(u"\N{euro sign}"),'amount':f"{round(avoir_item.item.unit_price*avoir_item.quantity_demanded,2)}%s"%(u"\N{euro sign}"),'reason':avoir_item.reason})  
                demande_date = None
                if avoir.date_created:
                    demande_date = f"{DAYS_OF_THE_WEEK[avoir.date_created.weekday()]} {str(avoir.date_created.day)} {MONTHS[avoir.date_created.month-1]}"
                data = {
                'restaurant_name': 'Kitchen Ter(r)e',
                'address': '12 rue Lanneau',
                'postal_code_and_city': '75005 Paris',
                'client_name': 'Anton Sirgue',
                'commande_number':commande.commande_number,
                'bl_number':commande.bon_livraison.number,
                'fournisseur_name':commande.fournisseur.name,
                'fournisseur_postal_code_and_city':'75006 Paris',
                'demande_date':demande_date,
                'ordering_mean':commande.ordering_mean,
                'restaurant_email':'email@memail.com',
                'restaurant_phone_number':'0678765645',
                'items':pdf_items,
                }
                pdf = render_to_pdf('pdfs/avoir.html',data)
                return HttpResponse(pdf, content_type='application/pdf',status=status.HTTP_201_CREATED)
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
                        commande.save()
                        commande_item.save()
                else:
                    return Response({"message":"Computation was not finished"},status=status.HTTP_400_BAD_REQUEST)
            try:
                commande.status = "AVOIR_RECEIVED_WAITING_INVOICE"
                commande.save()
                avoir = commande.avoir
                avoir.date_received = date.today()
                total_amount = 0
                for item in avoir.items.all():
                    total_amount += item.item.unit_price *item.quantity_received
                avoir.total_amount_ht = total_amount
                print("HHHHICNEJCNE")
                print(total_amount)
                commande.estimated_ht_total_cost = commande.estimated_ht_total_cost - total_amount
                print(commande.estimated_ht_total_cost)
                commande.save()
                avoir.save()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)


class ReceiveInvoiceAPIView(APIView):
    # parser_classes = [FileUploadParser]
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404
        
    def post(self, request, commande_id, format=None):
        commande = self.get_object(commande_id)
        if commande.status =="WAITING_INVOICE" or commande.status =="AVOIR_RECEIVED_WAITING_INVOICE":
            try: 
                print(request)
                print(request.data)
                file_obj = request.data['file']
                print("FILE OBJECT GOOD")
                commande = self.get_object(commande_id)
                print("COMMANDE GOOD")
                result = TextractWrapper().analyze_file(commande,file_obj)
                print("RESULKT")
                return Response(result,status=status.HTTP_200_OK)
            except Exception as e:
                print("IN HERE")
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, commande_id, format=None):
        commande = self.get_object(commande_id)
        if commande.status =="WAITING_INVOICE" or commande.status =="AVOIR_RECEIVED_WAITING_INVOICE":
            if self.update_commande_items(request.data):
                if self.create_invoice_for_commande(request.data,commande):
                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)         
        else:
            return Response({"message":"Wrong status"},status=status.HTTP_400_BAD_REQUEST)

    def clean_request_data_items(self,data):
        items = []
        for item in data['items']:
            item_data = {}
            for key in item:
                if item[key]:
                    item_data[key] = item[key]
            items.append(item_data)
        return items

    def create_invoice_for_commande(self, data, commande):
        no_item_data = data
        del no_item_data['items']
        invoice_serializer = InvoiceSerializer(data=data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            try:
                commande.invoice = invoice
                commande.status = "CLOSED"
                commande.save()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            print(invoice_serializer.errors)
            return False
    
    def update_commande_items(self, data):
        print(data)
        for item in self.clean_request_data_items(data):
            try: 
                item_obj = CommandeItem.objects.get(id=item['id'])
                commande_item_serializer = CommandeItemAllFieldsSerializer(item_obj,data=item,partial=True)
                if commande_item_serializer.is_valid():
                    commande_item_serializer.save()
                else:
                    return False
            except Exception as e: 
                print(e)
                return False
            produit_changes = {}
            if 'unit_quantity' in item:
                produit_changes['quantity'] = item['unit_quantity']
            if 'unit_price' in item:
                produit_changes['price'] = item['unit_price']
            if 'unit' in item:
                produit_changes['unit'] = item['unit']
            try:
                produit = item_obj.produit
                produit_serializer = ProduitSerializer(produit,data=produit_changes,partial=True)
                if produit_serializer.is_valid():
                    produit_serializer.save()
                else:
                    print(commande_item_serializer.errors)
                    return False
            except Exception as e:
                print(e)
                return False
        return True
        
