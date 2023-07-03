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
    quantity = models.IntegerField(null=True,blank=True)
    unit = models.CharField(max_length=100,null=True)
    genres = models.ManyToManyField(RecetteGenre,blank=True)
    last_selling_price = models.DecimalField( max_digits=10, decimal_places=2,null=True)
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
    quantity = models.DecimalField(max_digits = 12, decimal_places=5,blank=False)
    unit = models.CharField(default="kilogramme",max_length=100)
    note = models.CharField(max_length=250,blank=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    section = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=True,null=True)

class SousRecette(models.Model):
    unit = models.CharField(max_length=100,blank=False,null=False)
    quantity = models.DecimalField(max_digits = 12, decimal_places=5,default =1)
    note =  models.CharField(max_length=250,blank=True)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    sous_recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='sous_recette')

    class Meta:
        constraints = [
          models.CheckConstraint(check=~models.Q(recette=models.F('sous_recette')), name='can_not_add_itself'),
        ]
    
class RecetteProgressionElement(models.Model):
    rank = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=False)
    text =  models.TextField()
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    section = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=True,null=True)

class RecetteSection(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(limit_value=0)], blank=False)
    name = models.CharField(max_length=200, blank=False)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)

class FournisseurCategory(models.Model):
    name = models.CharField(max_length=120, blank=False,primary_key=True)
    # author ? 

class FournisseurSpecialty(models.Model):
    name = models.CharField(max_length=120, blank=False,primary_key=True)
     # author ? 
    
class Fournisseur(models.Model):
    name = models.CharField(max_length=250, blank=False)
    last_order_time = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(FournisseurCategory,blank=False,on_delete=models.CASCADE)
    specialty = models.ForeignKey(FournisseurSpecialty,null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True)
    address_line_2 = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    client_code = models.CharField(max_length=100, blank=True)
    principal_phone_number = models.CharField(max_length=12, blank=True)
    ordering_phone_number = models.CharField(max_length=12, blank=True)
    accounting_phone_number = models.CharField(max_length=12, blank=True)
    principal_email = models.EmailField(max_length=50, blank=True)
    ordering_email = models.EmailField(max_length=50, blank=True)
    cc_sales_email = models.EmailField(max_length=50, blank=True)
    delivers_monday = models.BooleanField(default=True)
    delivers_tuesday = models.BooleanField(default=True)
    delivers_wednesday = models.BooleanField(default=True)
    delivers_thursday = models.BooleanField(default=True)
    delivers_friday = models.BooleanField(default=True)
    delivers_saturday = models.BooleanField(default=True)
    delivers_sunday = models.BooleanField(default=True)

class FournisseurBack(models.Model):
    created_on = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    # created_by = 
    original_information_source = models.ForeignKey(Fournisseur, blank=False, on_delete=models.CASCADE)

class Produit(models.Model):
    ingredient = models.ForeignKey(Ingredients, blank=False, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, blank=False, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    quantity = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    unit = models.CharField(max_length=75, blank=True)
    labels = models.ManyToManyField(Labels,blank= True)
    geographic_location = models.CharField(max_length=150, blank=True)

class ProduitBack(models.Model):
    created_on = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    # created_by = 
    original_information_source = models.ForeignKey(Produit, blank=False, on_delete=models.CASCADE)

class ProduitPriceTracker(models.Model):
    created_on = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    produit = models.ForeignKey(Produit, blank=False, on_delete=models.CASCADE)
    kilogramme_price = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])

class CommandeItem(models.Model):
    produit = models.ForeignKey(Produit,null=False, on_delete=models.CASCADE)
    unit = models.CharField(max_length=100)
    unit_quantity = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    quantity = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    pending_avoir = models.BooleanField(default=False)
    received_avoir =  models.BooleanField(default=False)
    kilogramme_price =  models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    unit_price =  models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])

class AvoirItem(models.Model):
    item = models.ForeignKey(CommandeItem,null=False, on_delete=models.CASCADE)
    quantity_demanded = models.DecimalField(max_digits = 7, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    quantity_received = models.DecimalField(max_digits = 7, decimal_places=2, blank=True,null=True,validators=[MinValueValidator(limit_value=0)])
    reason = models.CharField(max_length=250)

class BonLivraison(models.Model):
    number =  models.CharField(max_length=50,null=False, blank=False)
    date_created = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    total_amount_ht = models.DecimalField(max_digits = 8, decimal_places=2, blank=True,null=True,validators=[MinValueValidator(limit_value=0)])

class Invoice(models.Model):
    number =  models.CharField(max_length=50,null=False, blank=False)
    date_created = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    total_amount_ht = models.DecimalField(max_digits = 8, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    total_taxes = models.DecimalField(max_digits = 8, decimal_places=2, blank=True,null=True,validators=[MinValueValidator(limit_value=0)])

class Avoir(models.Model):
    number =  models.CharField(max_length=50,null=False, blank=False)
    date_created = models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    date_received = models.DateField(validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')],blank=True,null=True)
    total_amount_ht = models.DecimalField(max_digits = 8, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    items = models.ManyToManyField(AvoirItem, blank=False) 


class Commande(models.Model):
    class OrderingMeans(models.TextChoices):
        EMAIL = "Commandée par mail"
        PHONE = "Commandée au téléphone"
        IN_PERSON = "Commandée en physique"
        CASH_OUT = "Opérée en sortie de caisse"
    
    class OrderStatus(models.TextChoices):
        WAITING_INVOICE = "WAITING_INVOICE"
        WAITING_DELIVERY = "WAITING_DELIVERY"
        WAITING_AVOIR = "WAITING_AVOIR"
        AVOIR_RECEIVED_WAITING_INVOICE = "AVOIR_RECEIVED_WAITING_INVOICE"
        CLOSED = "CLOSED"

    fournisseur = models.ForeignKey(Fournisseur, null=False,blank=False, on_delete=models.CASCADE) 
    items = models.ManyToManyField(CommandeItem, blank=False) 
    estimated_ht_total_cost = models.DecimalField(max_digits = 8, decimal_places=2, blank=False,validators=[MinValueValidator(limit_value=0)])
    status = models.CharField(choices=OrderStatus.choices,max_length=100,blank=False,null=False,default="WAITING_DELIVERY")
    date_created =  models.DateField(default=datetime.date.today,validators=[
        MaxValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')])
    month = models.CharField(max_length=100,null=False)
    commande_number = models.CharField(max_length=6,null=False,unique=True)
    bon_livraison = models.ForeignKey(BonLivraison, null=True,blank=True, on_delete=models.SET_NULL) 
    avoir = models.ForeignKey(Avoir, null=True,blank=True, on_delete=models.SET_NULL) 
    invoice = models.ForeignKey(Invoice, null=True,blank=True, on_delete=models.SET_NULL) 
    expected_delivery_date = models.DateField(default=None,validators=[
        MinValueValidator(
            limit_value=date.today(),
            message='Date can not be later than today')],blank=True, null=True)
    concerned_with_avoir = models.BooleanField(default=False)
    ordering_mean = models.CharField(choices=OrderingMeans.choices,max_length=100,blank=False,null=False)



