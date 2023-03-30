from rest_framework import serializers
from core_routes.models import *

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
    category = IngredientsCategoriesSerializer(many=True,read_only=True)
    sub_category = IngredientsSubCategoriesSerializer(many=True,read_only=True)
    class Meta:
        model = Ingredients
        fields = ('id','name', 'description','illustration','labels','allergenes','conversion_to_kilo','unit','category','sub_category')
    
class RecettesCategoriesSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecettesCategories
        fields = '__all__'

class RecettesTastesSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecettesTastes
        fields = '__all__'

class RecettesInspirationsSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecettesInspirations
        fields = '__all__'
    
class RecettesGenresSerializer(serializers.ModelSerializer):
     class Meta:
        model= RecettesGenres
        fields = '__all__'

class RecettesSerializer(serializers.ModelSerializer):
    categories = RecettesCategoriesSerializer(many=True,read_only=True)
    tastes = RecettesTastesSerializer(many=True,read_only=True)
    inspirations = RecettesInspirationsSerializer(many=True,read_only=True)
    genres = RecettesGenresSerializer(many=True,read_only=True)
    class Meta:
        model = Recettes
        fields = '__all__'

class GetRecettesIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientsGetSerializer()
    class Meta:
        model = RecettesIngredients
        fields = ('ingredient', 'quantity', 'unit','buying_price')

class RecettesIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientsSerializer()
    class Meta:
        model = RecettesIngredients
        fields = '__all__'

class CreateRecettesIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecettesIngredients
        fields = '__all__'

class SousRecettesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousRecettes
        fields = '__all__'

class RecettesProgressionElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecettesProgressionElements
        fields = '__all__'

class GetRecettesPogressionElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecettesProgressionElements
        fields = ('ordering','text')
