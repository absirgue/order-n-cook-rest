from django.contrib import admin
from core_routes.models import *
# Register your models here.
admin.site.register(Ingredients)
admin.site.register(IngredientsCategories)   
admin.site.register(IngredientsSubCategories)    
admin.site.register(Allergenes)
admin.site.register(Labels) 
admin.site.register(Recette)        
admin.site.register(RecetteCategory)        
admin.site.register(RecetteGenre)        
admin.site.register(RecetteIngredient)     
admin.site.register(RecetteTaste)        
admin.site.register(RecetteProgressionElement)        
admin.site.register(RecetteSection)        

