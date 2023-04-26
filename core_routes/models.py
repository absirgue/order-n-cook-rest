import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Allergenes(models.Model):
    name = models.CharField(max_length=75, blank=False,unique=True)
    

class Labels(models.Model):
    name = models.CharField(max_length=75, blank=False,unique=True)
    description = models.TextField(blank=True)

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
    name = models.CharField(max_length=120, blank=False,primary_key=True)
    # author

class IngredientsSubCategories(models.Model):
    name = models.CharField(max_length=120, blank=False,primary_key=True)
    # author
class Ingredients(models.Model):
    name = models.CharField(max_length=120, blank=False)
    description = models.TextField(blank= True)
    illustration = models.FileField(upload_to='ingredients/',blank=True)
    labels = models.ManyToManyField(Labels,blank= True)
    allergenes = models.ManyToManyField(Allergenes,blank= True)
    conversion_to_kilo = models.DecimalField(max_digits = 12, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)],blank= True)
    unit = models.CharField(default="kilogramme",max_length=100,blank= True)
    category = models.ForeignKey(IngredientsCategories,on_delete=models.SET_NULL,null=True,blank= False)
    sous_category = models.ForeignKey(IngredientsSubCategories,on_delete=models.SET_NULL,null=True,blank= False)
    is_in_season_january = models.BooleanField(default=False)
    is_in_season_february = models.BooleanField(default=False)
    is_in_season_march = models.BooleanField(default=False)
    is_in_season_april = models.BooleanField(default=False)
    is_in_season_may = models.BooleanField(default=False)
    is_in_season_june = models.BooleanField(default=False)
    is_in_season_july = models.BooleanField(default=False)
    is_in_season_august = models.BooleanField(default=False)
    is_in_season_september = models.BooleanField(default=False)
    is_in_season_october = models.BooleanField(default=False)
    is_in_season_november = models.BooleanField(default=False)
    is_in_season_december = models.BooleanField(default=False)

class Conversions(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    unit = models.CharField(default="kilogramme",max_length=100)
    conversion_to_kilo = models.DecimalField(max_digits = 14, decimal_places=7, default=1,validators=[MinValueValidator(limit_value=0)])
    # author = 

class RecetteGenre(models.Model):
    name = models.CharField(max_length=100, blank=False,primary_key=True)

class RecetteTaste(models.Model):
    name = models.CharField(max_length=100, blank=False,primary_key=True)

class RecetteCategory(models.Model):
    name = models.CharField(max_length=100, blank=False,primary_key=True)

# add inspiration
class Recette(models.Model):
    class RecetteUnits(models.TextChoices):
        PERSONNE = "personne"
        GRAMME = "gramme"
        KILOGRAMME ="kilorgamme"
        LITTRE = "littre"
        CENTILITTRE = "centilittre"
    
    class Months(models.TextChoices):
        JANVIER = "Janvier"
        FEVRIER = "Février"
        MARS = "Mars"
        AVRIL = "Avril"
        MAI = "Mai"
        JUIN = "Juin"
        JUILLET = "Juillet"
        AOUT = "Août"
        SEPTEMBRE = "Septembre"
        OCTOBRE = "Octobre"
        NOVEMBRE = "Novembre"
        DECEMBRE = "Décembre"

        
    name = models.CharField(max_length=250,blank=False)
    quantity = models.IntegerField(blank=True,null=True)
    unit = models.CharField(choices=RecetteUnits.choices,max_length=100,null=True)
    genres = models.ManyToManyField(RecetteGenre,blank=True)
    category = models.ForeignKey(RecetteCategory,blank=True,null=True, on_delete=models.SET_NULL)
    tastes = models.ManyToManyField(RecetteTaste,blank=True)
    duration = models.IntegerField(validators=[MinValueValidator(limit_value=0)],blank=True,null=True)
    last_modification = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    selected_for_menu = models.BooleanField(default=False)
    selected_for_next_menu = models.BooleanField(default=False)
    coefficient = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    tva = models.IntegerField(validators=[MaxValueValidator(limit_value=100),MaxValueValidator(limit_value=0)],blank=True,null=True)
    season_start = models.CharField(choices=Months.choices,max_length=100,blank=True,null=True)
    season_end = models.CharField(choices=Months.choices,max_length=100,blank=True,null=True)
    temperature = models.IntegerField(blank=True,null=True)
    sous_vide_pression = models.DecimalField(max_digits=4,decimal_places=2,blank=True,null=True)
    sous_vide_soudure = models.DecimalField(max_digits=4,decimal_places=2,blank=True,null=True)
    is_to_modify = models.BooleanField(default=True)

    def selling_price(self):
        #Implement
        pass


# Add section idea
class RecetteIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits = 12, decimal_places=7)
    unit = models.CharField(default="kilogramme",max_length=100)
    note = models.CharField(max_length=250,blank=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    section = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=True,null=True)

class SousRecette(models.Model):
    unit = models.CharField(default="kilogramme",max_length=100)
    quantity = models.DecimalField(max_digits = 12, decimal_places=7, default=1)
    note =  models.CharField(max_length=250,blank=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    sous_recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='sous_recette')
    
class RecetteProgressionElement(models.Model):
    rank = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=False)
    text =  models.TextField()
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    section = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=True,null=True)

class RecetteSection(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=False)
    name = models.CharField(max_length=200, blank=False)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)





