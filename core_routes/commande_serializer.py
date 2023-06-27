from rest_framework import serializers
from core_routes.models import *
from datetime import datetime
from core_routes.helpers.helper_functions import get_conversion_rate, get_kilogramme_price,get_last_produit_price_tracker

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
    bl = serializers.SerializerMethodField()
    avoir = serializers.SerializerMethodField()
    facture = serializers.SerializerMethodField()
    nb_jours = serializers.SerializerMethodField()

    def get_avoir(self,instance):
        if instance.avoir:
            avoir_date = "demandé " + str(instance.avoir.date_created)
            if instance.avoir.date_received:
                avoir_date = "reçu " + str(instance.avoir.date_received)
            return {'value':instance.avoir.number,'date':avoir_date}
        return None
    
    def get_facture(self,instance):
        if instance.invoice:
            return {'value':instance.invoice.number,'date':instance.invoice.date_created}
        return None

    def get_bl(self,instance):
        if instance.bon_livraison:
            return {'value':instance.bon_livraison.number,'date':instance.bon_livraison.date_created}
        return None
        
    def get_cde(self,instance):
       return {"value":instance.commande_number, "date":instance.date_created}

    def get_nb_jours(self,instance):
        if instance.status == "WAITING_AVOIR" or instance.status == "WAITING_INVOICE":
            if instance.avoir:
                avoir = instance.avoir
                delta = datetime.now() - datetime.strptime(str(avoir.date_created), "%Y-%m-%d")
                return delta.days
            else:
                return None
        elif instance.status == "WAITING_INVOICE":
            if instance.bon_livraison:
                bl = instance.bon_livraison
                delta = datetime.now() - datetime.strptime(str(bl.date_created), "%Y-%m-%d")
                return delta.days
            else:
                return None
        elif instance.status == "AVOIR_RECEIVED_WAITING_INVOICE":
            if instance.avoir and instance.avoir.date_received:
                avoir = instance.avoir
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
        fields = ('id','fournisseur','cde','month','status','nb_jours','cde','bl','facture','avoir')
        
class CommandeItemAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeItem
        fields = '__all__'

class CommandeItemSerializer(serializers.ModelSerializer):
    conversion = serializers.SerializerMethodField()
    real = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    kilogramme_price = serializers.SerializerMethodField()
    number_of_units = serializers.SerializerMethodField()
    
    def get_number_of_units(self,instance):
        return instance.quantity
    
    def get_name(self,instance):
        return instance.produit.ingredient.name
    
    def get_kilogramme_price(self,instance):
        return get_kilogramme_price(instance.produit.ingredient,instance.unit,instance.unit_quantity,instance.unit_price)
    
    def get_conversion(self,instance):
        conversion_rate = get_conversion_rate(ingredientId=instance.produit.ingredient.id,unit=instance.unit)
        conversion_unit = ""
        conversion_quantity = 0
        kilogramme_equivalence = 0
        if conversion_rate:
            kilogramme_equivalence = float(instance.unit_quantity* instance.quantity) * float(conversion_rate)
            conversion_quantity = kilogramme_equivalence
            conversion_unit = "kg"
            if kilogramme_equivalence <0.1:
                conversion_quantity = kilogramme_equivalence *1000
                conversion_unit = "g"
        else:
            return None
        return {"unit":conversion_unit,"quantity":conversion_quantity}
    
    def get_real(self,instance):
        return {"unit":instance.unit,"quantity":{instance.unit_quantity}}
    
    def get_total_price(self,instance):
        return instance.quantity * instance.unit_price
    class Meta:
        model = CommandeItem
        fields = 'id','name','conversion','number_of_units','real','quantity','kilogramme_price','unit_price','total_price','pending_avoir','received_avoir'

class AvoirItemDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    def get_name(self,instance):
        return instance.item.produit.ingredient.name
    
    def get_unit_price(self,instance):
        return instance.item.unit_price
    
    def get_unit(self,instance):
        return instance.item.unit_quantity
    
    class Meta:
        model = AvoirItem
        fields = 'name','unit_price','unit','quantity_demanded','quantity_received','reason','id'

class AvoirJustItemsSerializer(serializers.ModelSerializer):
    items = AvoirItemDetailSerializer(many=True)

    class Meta:
        model = Avoir
        fields = ('items','id')


class CommandeDetailsSerializer(serializers.ModelSerializer):
    fournisseur = CommandeFournisseurSerializer()
    order_details = serializers.SerializerMethodField()
    delivery_details = serializers.SerializerMethodField()
    avoir_details = serializers.SerializerMethodField()
    invoice_details = serializers.SerializerMethodField()
    items = CommandeItemSerializer(many=True)
    avoir = AvoirJustItemsSerializer()

    def get_order_details(self, instance):
        return {"identifier":instance.commande_number, "date":instance.date_created, "means":instance.ordering_mean}

    def get_invoice_details(self, instance):
        if instance.invoice:
            invoice = Invoice.objects.get(id=instance.invoice)
            return {"identifier":invoice.number,"date":invoice.date_created,"amount_ht":invoice.total_amount_ht,"total_taxes":invoice.total_taxes}
        else:
            return None
        
    def get_delivery_details(self, instance):
        if instance.bon_livraison:
            bl = instance.bon_livraison
            return {"identifier":bl.number,"date":bl.date_created,"amount":bl.total_amount_ht}
        else:
            return None
    
    def get_avoir_details(self, instance):
        if instance.avoir:
            avoir =instance.avoir
            was_received = False
            avoir_date = avoir.date_created
            if instance.status == "AVOIR_RECEIVED_WAITING_INVOICE":
                avoir_date = avoir.date_received
                was_received = True
            return {"identifier":avoir.number,"date":avoir_date,"amount":avoir.total_amount_ht,"was_received":was_received}
        else:
            return None

    class Meta:
        model = Commande
        fields = 'id','status','concerned_with_avoir','fournisseur','expected_delivery_date','order_details','delivery_details','estimated_ht_total_cost','avoir_details','invoice_details','items','avoir'


class BonLivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonLivraison
        fields = '__all__'

class AvoirItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvoirItem
        fields = '__all__'

class AvoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avoir
        fields = '__all__'