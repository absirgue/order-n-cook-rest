from rest_framework import serializers
from core_routes.models import *
import decimal

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

class IngredientsGetSerializer(serializers.ModelSerializer):
    labels = LabelsSerializer(many=True,read_only=True)
    allergenes = AllergenesSerializer(many=True,read_only=True)
    season = serializers.SerializerMethodField()

    def get_season(self, instance):
        return [instance.is_in_season_january,instance.is_in_season_february,instance.is_in_season_march,instance.is_in_season_april,instance.is_in_season_may,instance.is_in_season_june,instance.is_in_season_july,instance.is_in_season_august,instance.is_in_season_september,instance.is_in_season_october,instance.is_in_season_november,instance.is_in_season_december]
    
    class Meta:
        model = Ingredients
        fields = ('id','name', 'description','illustration','labels','allergenes','category','sous_category','season')
    

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
            print(instance.name)
            print(index_season_end)
            print(index_season_start)
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
        return 12.30
    
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
    cost_ingredients = serializers.SerializerMethodField()
    ht_selling_price= serializers.SerializerMethodField()
    ttc_selling_price= serializers.SerializerMethodField()
    ttc_unit_selling_price= serializers.SerializerMethodField()

    def get_ingredients(self,instance):
        all_ingredients = RecetteIngredient.objects.filter(recette=instance)
        ingredients_value = []
        for ingredient in all_ingredients:
            ingedient_obj = {"id":ingredient.id,"ingredient_id":ingredient.ingredient.id,"name":ingredient.ingredient.name,"allergenes":AllergenesSerializer(ingredient.ingredient.allergenes,many=True).data,"unit":ingredient.unit,"quantity":str(float(str(ingredient.quantity))),"note":ingredient.note,"cost":12}
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
            print(instance.name)
            print(index_season_end)
            print(index_season_start)
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
    

    def get_ht_selling_price(self,instance):
        if instance.coefficient:
            return self.get_cost_ingredients(instance) * float(instance.coefficient)
        else:
            return None

    def get_numeric_value_ttc_selling_price(self,instance):
        if instance.tva:
            return decimal.Decimal(self.get_ht_selling_price(instance)) * (100 + instance.tva) / 100
        else: 
            return None
    
    def get_ttc_selling_price(self,instance):
        numeric_value = self.get_numeric_value_ttc_selling_price(instance)
        if numeric_value:
            return str(round(numeric_value, 2))
        else:
            return None

    def get_ttc_unit_selling_price(self,instance):
        ttc_selling_price = self.get_numeric_value_ttc_selling_price(instance)
        if ttc_selling_price and instance.quantity:
            numeric_value = ttc_selling_price / instance.quantity 
            return str(round(numeric_value, 2))
        else:
            return None
    
    def get_cost_ingredients(self,instance):
        return 12.3
    
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
        fields = ('id','ingredients','sous_recette','sections','progression_elements','name', 'tva','coefficient','cost_ingredients','quantity','unit','genres','category','tastes','duration','temperature','sous_vide_pression','sous_vide_soudure','selected_for_menu','selected_for_next_menu','season','ht_selling_price','ttc_selling_price','allergenes','ttc_unit_selling_price','is_to_modify')


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
    ingredient = IngredientsGetSerializer()
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

class IngredientOnlyNameSerializer(serializers.ModelSerializer):
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
    id = serializers.SerializerMethodField()

    def get_quantity(self,instance):
        # Weird structure to remove trailing 0s
        return str(float(str(instance.quantity)))
    
    def get_name(self,instance):
        return instance.sous_recette.name
    
    def get_id(self,instance):
        return instance.sous_recette.id
    
    def get_cost(self,instance):
        return 12

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
        fields = ('id','name','unit','quantity','allergenes','cost','note')

class RecetteProgressionElementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteProgressionElement
        fields = ('text','section','recette','text')
 