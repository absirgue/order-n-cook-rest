from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.commande_serializer import *
from rest_framework.views import APIView
import random
import string
from core_routes.utils import render_to_pdf,encode_html
from django.http import HttpResponse
from core_routes.email import send_order_email

DAYS_OF_THE_WEEK = ["Lundi","Mardi","Mercredi","Jeudi",'Vendredi',"Samedi","Dimanche"]
MONTHS = ["Janvier","Février","Mars","Avril",'Mai',"Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
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
                    print(commande_item_serializer.errors)
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
            commande = serializer.save()
            pdf_items = []
            for item in commande.items.all():
                pdf_items.append({'quantity':str(round(item.quantity*item.unit_quantity, 2)),'unit':item.unit,'produit_name':item.produit.ingredient.name,'unit_price':f"{item.unit_price}%s"%(u"\N{euro sign}"),'total_amount':f"{round(item.quantity*item.unit_price, 2)}%s"%(u"\N{euro sign}")})
            ht_total = 0
            for item in pdf_items:
                ht_total += float(item['total_amount'][:-1])
            ht_total = f"{str(round(ht_total, 2))}%s"%(u"\N{euro sign}")
            delivery_date = None
            if commande.expected_delivery_date:
                delivery_date = f"{DAYS_OF_THE_WEEK[commande.expected_delivery_date.weekday()]} {str(commande.expected_delivery_date.day)} {MONTHS[commande.expected_delivery_date.month-1]}"
            client_name = 'Anton Sirgue'
            client_email = "asbirgue@gmail.com"
            client_restaurant_name = "Kitchen Ter(r)e"
            data = {
            'restaurant_name': client_restaurant_name,
            'address': '12 rue Lanneau',
            'postal_code_and_city': '75005 Paris',
            'client_name': client_name,
            'cde_number':commande.commande_number,
            'fournisseur_name':commande.fournisseur.name,
            'fournisseur_postal_code_and_city':'75006 Paris',
            'expected_delivery_day_and_date':delivery_date,
            'commande_date':commande.date_created,
            'ordering_mean':commande.ordering_mean,
            'restaurant_email':client_email,
            'restaurant_phone_number':'0678765645',
            'items':pdf_items,
            'ht_total':ht_total
             }
            pdf = render_to_pdf('pdfs/commande.html',data)
            pdf_raw_bytes = pdf.getvalue()   
            if commande.ordering_mean == "Commandée par mail":
                if commande.fournisseur.ordering_email:
                    
                    send_order_email(client_email,commande.fournisseur.ordering_email,commande.commande_number,commande.fournisseur.name,client_restaurant_name,client_name,pdf,request.data['email_note'])
                else:
                    return HttpResponse(pdf_raw_bytes, content_type='application/pdf',status=status.HTTP_202_ACCEPTED)
            return HttpResponse(pdf_raw_bytes, content_type='application/pdf',status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
