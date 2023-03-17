from rest_framework import serializers
from core_routes.models import Allergenes,Labels,Ingredients,Conversions

class AllergenesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Allergenes
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
    class Meta:
        model = Ingredients
        fields = ('id','name', 'description','illustration','labels','allergenes','conversion_to_kilo','unit')
    