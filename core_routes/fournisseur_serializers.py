from rest_framework import serializers
from core_routes.models import *
from core_routes.serializers import IngredientsListSerializer
from core_routes.helpers.helper_functions import get_conversion_rate, get_kilogramme_price,get_last_produit_price_tracker
from core_routes.serializers import LabelsSerializer


class FournisseurListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fournisseur
        fields = ('id','name','category','specialty','delivers_monday','delivers_tuesday','delivers_wednesday','delivers_thursday','delivers_friday','delivers_saturday','delivers_sunday')

class FournisseurAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Fournisseur
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model= Produit
        fields = '__all__'

class ProduitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= Produit
        fields = '__all__'

class ProduitWithIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientsListSerializer(read_only=True)
    real_unit = serializers.SerializerMethodField()
    conversion_unit = serializers.SerializerMethodField()
    labels = LabelsSerializer(read_only=True,many=True)
    kilogramme_price = serializers.SerializerMethodField()
    last_known_price = serializers.SerializerMethodField()
    date_last_known_price = serializers.SerializerMethodField()

    def get_real_unit(self,instance):
        return {"unit":instance.unit,"quantity":instance.quantity}

    def get_conversion_unit(self,instance):
            conversion_rate = get_conversion_rate(ingredientId=instance.ingredient.id,unit=instance.unit)
            conversion_unit = ""
            conversion_quantity = 0
            kilogramme_equivalence = 0
            if conversion_rate:
                kilogramme_equivalence = float(instance.quantity) * float(conversion_rate)
                conversion_quantity = kilogramme_equivalence
                conversion_unit = "kg"
                if kilogramme_equivalence <0.1:
                    conversion_quantity = kilogramme_equivalence *1000
                    conversion_unit = "g"
            else:
               return None
            
            return {"unit":conversion_unit,"quantity":conversion_quantity}
            
    def get_kilogramme_price(self, instance):
        return get_kilogramme_price(instance.ingredient,instance.unit,instance.quantity,instance.price)

    def get_last_known_price(self,instance):
        return str(get_last_produit_price_tracker(instance).kilogramme_price) + "€/kg"
    
    def get_date_last_known_price(self,instance):
        return get_last_produit_price_tracker(instance).created_on.strftime("%d/%m/%Y")
  
    class Meta:
        model= Produit
        fields = ('id','price','ingredient','real_unit','conversion_unit','kilogramme_price','last_known_price','date_last_known_price','labels')


class FournisseurDetailSerializer(serializers.ModelSerializer):
    produits = serializers.SerializerMethodField()

    def get_produits(self,instance):
        produits = Produit.objects.filter(fournisseur=instance.id)
        return ProduitWithIngredientSerializer(produits,many=True).data
        

    class Meta:
        model= Fournisseur
        fields = ('id','name','last_order_time','category','specialty','address','address_line_2','postal_code','city','department','country','client_code','principal_phone_number',
                  'ordering_phone_number','accounting_phone_number','principal_email','ordering_email','cc_sales_email','delivers_monday','delivers_tuesday','delivers_wednesday','delivers_thursday','delivers_friday','delivers_saturday','delivers_sunday','produits')

class ForunisseurCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= FournisseurCategory
        fields = '__all__'

class ForunisseurSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model= FournisseurSpecialty
        fields = '__all__'
   

    