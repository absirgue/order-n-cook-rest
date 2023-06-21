from rest_framework import serializers
from core_routes.models import *
from datetime import datetime

class CommandeAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'

class CommandeFournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = ('name','category','specialty')

class CommandeListSerializer(serializers.ModelSerializer):
    fournisseur = CommandeFournisseurSerializer()
    cde = serializers.SerializerMethodField()
    nb_jours = serializers.SerializerMethodField()

    def get_cde(self,instance):
       return {"value":instance.commande_number, "date":instance.date_created}

    def get_nb_jours(self,instance):
        if instance.status == "WAITING_AVOIR" or instance.status == "WAITING_INVOICE":
            if instance.avoir:
                avoir = Avoir.objects.get(id=instance.avoir)
                delta = datetime.now() - datetime.strptime(str(avoir.date_created), "%Y-%m-%d")
                return delta.days
            else:
                return None
        elif instance.status == "WAITING_INVOICE":
            if instance.bon_livraison:
                bl = BonLivraison.objects.get(id=instance.bon_livraison)
                delta = datetime.now() - datetime.strptime(str(bl.date_created), "%Y-%m-%d")
                return delta.days
            else:
                return None
        elif instance.status == "AVOIR_RECEIVED_WAITING_INVOICE":
            if instance.avoir:
                avoir = Avoir.objects.get(id=instance.avoir)
                delta = datetime.now() - datetime.strptime(str(avoir.date_received), "%Y-%m-%d")
                return delta.days
            else:
                return None
        elif instance.status == "CLOSED":
            return None
        else:
            if instance.date_created:
                delta = datetime.now() -  datetime.strptime(str(instance.date_created), "%Y-%m-%d")
                return delta.days
            else:
                return None
    
    
    class Meta:
        model = Commande
        fields = ('id','fournisseur','cde','month','status','nb_jours')
        
class CommandeItemAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeItem
        fields = '__all__'