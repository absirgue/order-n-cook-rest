import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date

class Allergenes(models.Model):
    name = models.CharField(max_length=75, blank=False)

class Labels(models.Model):
    name = models.CharField(max_length=75, blank=False)

class Unites(models.TextChoices):
        GRAMME = "gramme"
        KILOGRAMME = "kilogramme"
        CENTILITTRE = "centilittre"
        LITTRE = "littre"
        UNITE = "unité"
        CUILLERE_A_SOUPE = "table_spoon"
        CUILLERE_A_CAFE = "tea_spoon"
        CUP = "cup"

class IngredientsCategories(models.Model):
    name = models.CharField(max_length=120, blank=False)
    # author

class IngredientsSubCategories(models.Model):
    models.CharField(max_length=120, blank=False)
    # author
class Ingredients(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField(blank= True)
    illustration = models.FileField(upload_to='ingredients/',blank=True)
    labels = models.ManyToManyField(Labels,blank= True)
    allergenes = models.ManyToManyField(Allergenes,blank= True)
    conversion_to_kilo = models.DecimalField(max_digits = 12, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)],blank= True)
    unit = models.CharField(default="kilogramme",max_length=100,blank= True)
    category = models.OneToOneField(IngredientsCategories,on_delete=models.SET_NULL,null=True,blank= True)
    sub_category = models.OneToOneField(IngredientsSubCategories,on_delete=models.SET_NULL,null=True,blank= True)

class Conversions(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    unit = models.CharField(default="kilogramme",max_length=100)
    conversion_to_kilo = models.DecimalField(max_digits = 14, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)])
    # author = 

class RecettesGenres(models.Model):
    name = models.CharField(max_length=100, blank=False)
class RecettesTastes(models.Model):
    name = models.CharField(max_length=100, blank=False)

class RecettesInspirations(models.Model):
    name = models.CharField(max_length=100, blank=False)

class RecettesCategories(models.Model):
    name = models.CharField(max_length=100, blank=False)

# add inspiration
class Recettes(models.Model):
    class RecetteUnits(models.TextChoices):
        PERSONNE = "personne"
        GRAMME = "gramme"
        KILOGRAMME ="kilorgamme"
        LITTRE = "littre"
        CENTILITTRE = "centilittre"
    name = models.CharField(max_length=250)
    quantity = models.IntegerField(blank=False)
    # let free
    unit = models.CharField(choices=RecetteUnits.choices, default="personne",max_length=100)
    genres = models.ManyToManyField(RecettesGenres,blank=True)
    categories = models.ManyToManyField(RecettesCategories,blank=True)
    tastes = models.ManyToManyField(RecettesTastes,blank=True)
    inspirations = models.ManyToManyField(RecettesInspirations,blank=True)
    # Add validator
    duration = models.IntegerField()
    last_modification = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    selected_for_menu = models.BooleanField(default=False)
    # selling_price = models.DecimalField(max_digits=6,decimal_places=2,null=True)
    # Add validator (<100)
    tva = models.DecimalField(max_digits=5,decimal_places=2,null=True)

    def selling_price(self):
        #Implement
        pass

# make a IngredientsPourRecettes model that stors buying price.
class RecettesIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10,decimal_places=3)
    unit = models.CharField(choices=Unites.choices, default="kilogramme",max_length=100)
    # Add validator
    buying_price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE)

class SousRecettes(models.Model):
    unit = models.CharField(choices=Unites.choices, default="kilogramme",max_length=100)
    quantity_in_kilogramme = models.DecimalField(max_digits = 12, decimal_places=7, default=1)
    # Add validator
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE)
    sous_recette = models.ForeignKey(Recettes, on_delete=models.CASCADE, related_name='sous_recette')
    
class RecettesPogressionElements(models.Model):
    # Add validator
    ordering = models.IntegerField()
    text =  models.TextField()
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE)







