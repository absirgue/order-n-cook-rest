from rest_framework import serializers
from core_routes.models import *
from core_routes.helpers.helper_functions import get_conversion_rate, get_kilogramme_price, get_recette_ingredient_cost,get_raw_cost_for_recette_instance,get_ht_selling_price,get_ttc_unit_selling_price

class AllergenesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Allergenes
        fields = '__all__'

class IngredientsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= IngredientsCategories
        fields = '__all__'

class IngredientsSubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= IngredientsSubCategories
        fields = '__all__'

class ConversionsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Conversions
        fields = '__all__'


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields = '__all__'

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ingredients
        fields = '__all__'

class IngredientsListSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True,read_only=True)
    allergenes = AllergenesSerializer(many=True,read_only=True)
    season = serializers.SerializerMethodField()

    def get_season(self, instance):
        return [instance.is_in_season_january,instance.is_in_season_february,instance.is_in_season_march,instance.is_in_season_april,instance.is_in_season_may,instance.is_in_season_june,instance.is_in_season_july,instance.is_in_season_august,instance.is_in_season_september,instance.is_in_season_october,instance.is_in_season_november,instance.is_in_season_december]
    
    class Meta:
        model = Ingredients
        fields = ('id','name', 'description','illustration','labels','allergenes','category','sous_category','season')

class IngredientsDetailSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True,read_only=True)
    allergenes = AllergenesSerializer(many=True,read_only=True)
    season = serializers.SerializerMethodField()
    associated_produits = serializers.SerializerMethodField()

    def get_associated_produits(self,instance):
        produits = Produit.objects.filter(ingredient=instance)
        return ProduitForIngredientSerializer(produits,many=True).data


    def get_season(self, instance):
        return [instance.is_in_season_january,instance.is_in_season_february,instance.is_in_season_march,instance.is_in_season_april,instance.is_in_season_may,instance.is_in_season_june,instance.is_in_season_july,instance.is_in_season_august,instance.is_in_season_september,instance.is_in_season_october,instance.is_in_season_november,instance.is_in_season_december]
    
    class Meta:
        model = Ingredients
        fields = ('id','name', 'description','illustration','labels','allergenes','category','sous_category','season','associated_produits')

class ProduitForIngredientSerializer(serializers.ModelSerializer):
    real_unit = serializers.SerializerMethodField()
    conversion_unit = serializers.SerializerMethodField()
    labels = LabelsSerializer(read_only=True,many=True)
    kilogramme_price = serializers.SerializerMethodField()
    fournisseur_name = serializers.SerializerMethodField()
    fournisseur_id = serializers.SerializerMethodField()

    def get_fournisseur_name(self,instance):
        return instance.fournisseur.name

    def get_fournisseur_id(self,instance):
        return instance.fournisseur.id

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


    class Meta:
        model= Produit
        fields = 'id','price','fournisseur_name','fournisseur_id','real_unit','conversion_unit','kilogramme_price','geographic_location','labels'

class RecetteListGetSerializer(serializers.ModelSerializer):
    season = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    allergenes = serializers.SerializerMethodField()

    def get_season(self,instance):
        if instance.season_start and instance.season_end:
            months = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
            season = []
            index_season_start = months.index(instance.season_start.lower())
            index_season_end = months.index(instance.season_end.lower())
            if index_season_start > index_season_end:
                for i in range (12, index_season_start-2,-1):
                    season.append(True)
                for i in range (index_season_start-1, index_season_end,-1):
                    season.append(False)
                for i in range (index_season_end-1, 0,-1):
                    season.append(True)
            else:
                for i in range (0, index_season_start):
                    season.append(False)
                for i in range (index_season_start, index_season_end+1):
                    season.append(True)
                for i in range (index_season_end+1, 12):
                    season.append(False)
            return season
        else:
            return None

    def get_selling_price(self,instance):
        return_obj = {}
        raw_material_cost = get_raw_cost_for_recette_instance(instance)
        ht_cost = get_ht_selling_price(instance,raw_material_cost)
        unit_ttc_selling_price = get_ttc_unit_selling_price(instance,ht_cost)
        if unit_ttc_selling_price:
            return_obj["price"] = unit_ttc_selling_price
        else:
            return_obj["price"] = "-"
        if instance.last_selling_price and unit_ttc_selling_price:
            if unit_ttc_selling_price < instance.last_selling_price:
              return_obj["evolution"] = "LOWER"
            elif unit_ttc_selling_price > instance.last_selling_price:
                return_obj["evolution"]= "HIGHER"
            else:
                 return_obj["evolution"]= "SAME"
        if unit_ttc_selling_price:
            instance.last_selling_price = unit_ttc_selling_price
            instance.save()
        return return_obj

    def get_allergenes(self,instance):
        instance_ingredients = RecetteIngredient.objects.filter(recette=instance)
        allergenes = []
        for ingredient in instance_ingredients:
            allergenes.append(AllergenesSerializer(ingredient.ingredient.allergenes,many=True).data)
        unique_allergenes = []
        for sublist in allergenes:
            for allergene in sublist:
                if allergene not in unique_allergenes:
                    unique_allergenes.append(allergene)
      
        return unique_allergenes

    class Meta:
        model = Recette
        fields = ('id','name', 'quantity','unit','genres','is_to_modify','category','tastes','selected_for_menu','selected_for_next_menu','season','selling_price','allergenes')

class RecetteDetailGetSerializer(serializers.ModelSerializer):
    season = serializers.SerializerMethodField()
    allergenes = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    sous_recette = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()
    progression_elements = serializers.SerializerMethodField()
   

    def get_ingredients(self,instance):
        all_ingredients = RecetteIngredient.objects.filter(recette=instance)
        ingredients_value = []
        for ingredient in all_ingredients:
            ingedient_obj = {"id":ingredient.id,"ingredient_id":ingredient.ingredient.id,"name":ingredient.ingredient.name,"allergenes":AllergenesSerializer(ingredient.ingredient.allergenes,many=True).data,"unit":ingredient.unit,"quantity":str(float(str(ingredient.quantity))),"note":ingredient.note,"cost":get_recette_ingredient_cost(ingredient)}
            if ingredient.section:
                ingedient_obj["section"] = ingredient.section
            ingredients_value.append(ingedient_obj)
        return ingredients_value
    
    def get_sous_recette(self,instance):
        all_sous_recette = SousRecette.objects.filter(recette=instance)
        return GetSousRecetteSerializer(all_sous_recette,many=True).data
    
    def get_progression_elements(self,instance):
        all_progression_elements = RecetteProgressionElement.objects.filter(recette=instance)
        progression_elements = []
        for progression_element in all_progression_elements:
            progression_elements.append({"id":progression_element.id,"text":progression_element.text,"rank":progression_element.rank,"section":progression_element.section})
        return progression_elements
    
    def get_sections(self,instance):
        all_sections = RecetteSection.objects.filter(recette=instance)
        progression_sections = []
        for section in all_sections:
            progression_sections.append({"id":section.id,"name":section.name,"number":section.number})
        return progression_sections

    def get_season(self,instance):
        if instance.season_start and instance.season_end:
            months = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
            season = []
            index_season_start = months.index(instance.season_start.lower())
            index_season_end = months.index(instance.season_end.lower())
            if index_season_start > index_season_end:
                for i in range (12, index_season_start-2,-1):
                    season.append(True)
                for i in range (index_season_start-1, index_season_end,-1):
                    season.append(False)
                for i in range (index_season_end-1, 0,-1):
                    season.append(True)
            else:
                for i in range (0, index_season_start):
                    season.append(False)
                for i in range (index_season_start, index_season_end+1):
                    season.append(True)
                for i in range (index_season_end+1, 12):
                    season.append(False)
            return season
        else:
            return None
    

    
    def get_allergenes(self,instance):
        instance_ingredients = RecetteIngredient.objects.filter(recette=instance)
        allergenes = []
        for ingredient in instance_ingredients:
            allergenes.append(AllergenesSerializer(ingredient.ingredient.allergenes,many=True).data)
        unique_allergenes = []
        for sublist in allergenes:
            for allergene in sublist:
                if allergene not in unique_allergenes:
                    unique_allergenes.append(allergene)
      
        return unique_allergenes

    class Meta:
        model = Recette
        fields = ('id','ingredients','sous_recette','sections','progression_elements','name', 'tva','coefficient','quantity','unit','genres','category','tastes','duration','temperature','sous_vide_pression','sous_vide_soudure','selected_for_menu','selected_for_next_menu','season','is_to_modify','allergenes')


class RecetteCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model= RecetteCategory
        fields = '__all__'

class RecetteTasteSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecetteTaste
        fields = '__all__'
    
class RecetteGenreSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecetteGenre
        fields = '__all__'

class RecetteSerializer(serializers.ModelSerializer):
    # categories = RecetteCategorySerializer(many=True)
    # tastes = RecetteTasteSerializer(many=True)
    # genres = RecetteGenreSerializer(many=True)
    class Meta:
        model = Recette
        fields = '__all__'

class GetRecetteIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientsListSerializer()
    class Meta:
        model = RecetteIngredient
        fields = ('ingredient', 'quantity', 'unit','buying_price')

class RecetteIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientsSerializer()
    class Meta:
        model = RecetteIngredient
        fields = '__all__'

class CreateRecetteIngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecetteIngredient
        fields = '__all__'
    

class SousRecetteSerializer(serializers.ModelSerializer):

    def validate_sous_recette(self,sous_recette):
        if not (sous_recette.unit and sous_recette.quantity):
            raise serializers.ValidationError("Cette recette ne peut pas être une sous recette car sa quantité et son unité sont inconnues.")
        else:
            return sous_recette
        
    class Meta:
        model = SousRecette
        fields = '__all__'

class RecetteProgressionElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteProgressionElement
        fields = '__all__'

class GetRecettePogressionElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteProgressionElement
        fields = ('ordering','text')


class IngredientUnitsAndLabelsSerializer(serializers.ModelSerializer):
    units = serializers.SerializerMethodField()
    labels = LabelsSerializer(many=True,read_only=True)
    def get_units(self,instance):
        units = ["kilogramme"]
        if instance.unit != "kilogramme":
                units.append(instance.unit)
            
        try:
            recorded_conversions = Conversions.objects.filter(ingredient=instance)
            for conversion in recorded_conversions:
                units.append(conversion.unit)
           
        except:
            pass
        return units
        
    class Meta:
        model = Ingredients
        fields = ('id','name','units','labels')

class IngredientAndUnitsSerializer(serializers.ModelSerializer):
    units = serializers.SerializerMethodField()

    def get_units(self,instance):
        units = ["kilogramme"]
        if instance.unit != "kilogramme":
                units.append(instance.unit)
            
        try:
            recorded_conversions = Conversions.objects.filter(ingredient=instance)
            for conversion in recorded_conversions:
                units.append(conversion.unit)
           
        except:
            pass
        return units
        
    class Meta:
        model = Ingredients
        fields = ('id','name','units')

class SousRecetteOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recette
        fields = ('id','name','unit')

class RecetteSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteSection
        fields = '__all__'

class GetSousRecetteSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    allergenes = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    sous_recette_id = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    def get_cost(self, instance):
        return get_raw_cost_for_recette_instance(instance.sous_recette) * float(instance.quantity)/float(instance.sous_recette.quantity)

    def get_quantity(self,instance):
        # Weird structure to remove trailing 0s
        return str(float(str(instance.quantity)))
    
    def get_name(self,instance):
        return instance.sous_recette.name
    
    def get_sous_recette_id(self,instance):
        return instance.sous_recette.id

    def get_allergenes(self,instance):
        instance_ingredients = RecetteIngredient.objects.filter(recette=instance.sous_recette)
        allergenes = []
        for ingredient in instance_ingredients:
            allergenes.append(AllergenesSerializer(ingredient.ingredient.allergenes,many=True).data)
        unique_allergenes = []
        for sublist in allergenes:
            for allergene in sublist:
                if allergene not in unique_allergenes:
                    unique_allergenes.append(allergene)
      
        return unique_allergenes
    
    class Meta:
        model = SousRecette
        fields = ('sous_recette_id','id','name','unit','quantity','allergenes','cost','note','recette')

class RecetteProgressionElementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteProgressionElement
        fields = ('text','section','recette','text')
 