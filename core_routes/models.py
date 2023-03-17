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
        CUILLERE_A_CAFE = "teas_spoon"
        CUP = "cup"

class Ingredients(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField()
    illustration = models.FileField(upload_to='ingredients/',blank=True)
    labels = models.ManyToManyField(Labels)
    allergenes = models.ManyToManyField(Allergenes)
    conversion_to_kilo = models.DecimalField(max_digits = 12, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)])
    unit = models.CharField(default="kilogramme",max_length=100)

class Conversions(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    unit = models.CharField(default="kilogramme",max_length=100)
    conversion_to_kilo = models.DecimalField(max_digits = 14, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)])
    # author = 

class RecettesGenres(models.Model):
    name = models.CharField(max_length=100, blank=False)

class RecettesTastes(models.Model):
    name = models.CharField(max_length=100, blank=False)

class RecettesInsipirations(models.Model):
    name = models.CharField(max_length=100, blank=False)

class RecettesCategories(models.Model):
    name = models.CharField(max_length=100, blank=False)

class Recettes(models.Model):
    class RecetteUnits(models.TextChoices):
        PERSONNE = "personne"
        GRAMME = "gramme"
        KILOGRAMME ="kilorgamme"
        LITTRE = "littre"
        CENTILITTRE = "centilittre"

    quantity = models.IntegerField(blank=False)
    unit = models.CharField(choices=RecetteUnits.choices, default="personne",max_length=100)
    genre = models.ManyToManyField(RecettesGenres)
    category = models.ManyToManyField(RecettesCategories)
    taste = models.ManyToManyField(RecettesTastes)
    # Add validator
    duration = models.IntegerField()
    last_modification = models.DateField(default=timezone.now,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    selected_for_menu = models.BooleanField(default=False)
    selling_price = models.DecimalField(max_digits=6,decimal_places=2)
    tva = models.DecimalField(max_digits=5,decimal_places=2)

class RecettesIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10,decimal_places=3)
    unit = models.CharField(choices=Unites.choices, default="kilogramme",max_length=100)
    quantity_in_kilogramme = models.DecimalField(max_digits = 12, decimal_places=7, default=1)
    # Add validator
    buying_price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE)
    
class RecettesPogressionElement(models.Model):
    # Add validator
    ordering = models.IntegerField()
    text =  models.TextField()
    recette = models.ForeignKey(Recettes, on_delete=models.CASCADE)







