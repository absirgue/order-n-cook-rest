# This file is bound to be refactored. Will hold all helper functions until refactoring becomes a need.

# Return the conversion rate from an ingredient to a unit to kilogramme.
from core_routes.models import Conversions, Ingredients, ProduitPriceTracker,Produit,SousRecette,RecetteIngredient,Recette
import decimal


def get_conversion_rate(ingredientId, unit):
    try:
        if unit == "kilogramme":
            return 1  
        ingredient = Ingredients.objects.get(id=ingredientId)
        default_conversion_rate = get_default_conversion_rate(ingredient, unit)
        if default_conversion_rate:
            return default_conversion_rate
        recorded_conversion = get_recorded_conversion_rate(ingredient, unit)
        if recorded_conversion:
            return recorded_conversion
        return 0
    except:
        return 0

# Return the conversion rate from an ingredient's default unit to kilogramme if the default unit is the one 
# searched for. Otherwise, or if error, returns 0.
def get_default_conversion_rate(ingredient, unit):
    try:
        if ingredient.unit == unit:
            return ingredient.conversion_to_kilo
        else:
            return 0
    except:
        return 0
    
# Return the conversion rate from a quantity of an ingredient in a certain unit to kilogramme
# based on the Conversions record. Returns 0 if such conversion rate does not exist.
def get_recorded_conversion_rate(ingredient, unit):
    try:
        return Conversions.objects.get(ingredient=ingredient,unit=unit).conversion_to_kilo
    except:
        return 0
    
def get_kilogramme_price(ingredient,unit,quantity,price):
    conversion_rate = get_conversion_rate(ingredientId=ingredient.id,unit=unit)
    kilogramme_equivalence = 0
    if conversion_rate:
        kilogramme_equivalence = float(quantity) * float(conversion_rate)
                
    if kilogramme_equivalence == 0 :
            return "X"
    else:
        return round(float(price) / kilogramme_equivalence, 2)
    
def get_last_produit_price_tracker(produit):
    return ProduitPriceTracker.objects.filter(produit=produit).order_by('-created_on')[0]

def get_recette_ingredient_cost(recette_ingredient):
        produits_for_ingredient = Produit.objects.filter(ingredient=recette_ingredient.ingredient)
        if produits_for_ingredient:
            needed_quantity_in_kg = float(get_conversion_rate(recette_ingredient.ingredient.id,recette_ingredient.unit))*float(recette_ingredient.quantity)
            min_cost = 1000000000
            for produit in produits_for_ingredient :
                kg_price = get_kilogramme_price(recette_ingredient.ingredient,produit.unit,produit.quantity,produit.price)
                cost = kg_price*needed_quantity_in_kg
                if  cost< min_cost:
                    min_cost = cost
            return min_cost 
        else:
            return None


def get_ht_selling_price(recette,cost_ingredients):
    if recette.coefficient:
        return cost_ingredients * float(recette.coefficient)
    else:
        return None

def get_numeric_value_ttc_selling_price(recette,ht_selling_price):
    if recette.tva and ht_selling_price:
        return decimal.Decimal(ht_selling_price) * (100 + recette.tva) / 100
    else: 
        return None
    
def get_ttc_selling_price(recette,ht_selling_price):
    numeric_value = get_numeric_value_ttc_selling_price(recette,ht_selling_price)
    if numeric_value:
        return str(round(numeric_value, 2))
    else:
        return None

def get_ttc_unit_selling_price(recette,ht_selling_price):
    ttc_selling_price = get_numeric_value_ttc_selling_price(recette,ht_selling_price)
    print("ttc_selling_price")
    print(ttc_selling_price)
    print(recette.quantity)
    if ttc_selling_price and recette.quantity:
        numeric_value = ttc_selling_price / recette.quantity 
        return round(numeric_value, 2)
    else:
         return None
    
def get_raw_cost_from_serialized_recette(serialized_recette):
    cost = 0
    if serialized_recette["ingredients"]:
        for ingredient in serialized_recette["ingredients"]:
            if ingredient["cost"]:
                cost += ingredient["cost"]
    if serialized_recette["sous_recette"]:
        for sous_recette in serialized_recette["sous_recette"]:
            if sous_recette["cost"]:
                cost += sous_recette["cost"] 
    return cost

def get_raw_cost_for_recette_instance(recette_instance):
    print("TESTING FOR")
    print(recette_instance.name)
    ingredients_cost = 0
    for ingredient in RecetteIngredient.objects.filter(recette=recette_instance):
        cost = get_recette_ingredient_cost(ingredient)
        if cost:
            ingredients_cost+=cost
    
    print("iNGREIDENTS COST:" + str(ingredients_cost))
    if SousRecette.objects.filter(recette=recette_instance).exists():
        print("exists:")
        sous_recette_cost = 0
        for sous_recette in SousRecette.objects.filter(recette=recette_instance):
            # Add notion of share of recette
            sous_recette_cost += get_raw_cost_for_recette_instance(sous_recette.sous_recette) * (float(sous_recette.quantity)/float(sous_recette.sous_recette.quantity))
        return ingredients_cost + sous_recette_cost 
    else:
        return ingredients_cost 
    

def get_dependencies(recette_id):
    return get_downstream_depencies(recette_id) | get_upstream_depencies(recette_id)


def get_downstream_depencies(recette_id, visited=None):
    if visited is None:
        visited = set()
    visited.add(recette_id)

    for neighbor_recette in SousRecette.objects.filter(recette=recette_id).order_by("id"):
        if neighbor_recette.sous_recette.id not in visited:
            neighbor_recette_id = neighbor_recette.sous_recette.id
            get_downstream_depencies(neighbor_recette_id, visited)
    return visited

def get_upstream_depencies(recette_id, visited=None):
    if visited is None:
        visited = set()
    visited.add(recette_id)

    for neighbor_recette in SousRecette.objects.filter(sous_recette=recette_id).order_by("id"):
        if neighbor_recette.recette.id not in visited:
            neighbor_recette_id = neighbor_recette.recette.id
            get_upstream_depencies(neighbor_recette_id, visited)
    return visited

def get_recette_dependency_list(recette):
    downstream_depedencies = get_downstream_dependencies(recette)

def get_downstream_dependencies(recette,stack,result_list):
    stack += SousRecette.objects.filter(recette = recette)
    if len(stack) == 0:
        return result_list.append(recette.id)
    else:
        r



def get_all_excluded_recette_ids_downstream(list,recette):
    if SousRecette.objects.filter(recette=recette).exists():
        children = SousRecette.objects.filter(recette=recette).order_by('id')
        for recette in children:
            list = get_all_excluded_recette_ids_downstream(list,recette.sous_recette)
        print(list)
        list.append(recette.id)
        return list
    else:
        print("HERE:"+str(list))
        print("HERE:"+recette.name)
        print("HERE:"+str(recette.id))
        list.append(recette.id)
        print("WILL RETURN:"+str(list))
        return list

def get_all_excluded_recette_ids_upstream(list,recette):
    if SousRecette.objects.filter(sous_recette=recette).exists():
        children = SousRecette.objects.filter(sous_recette=recette).order_by('id')
        for recette in children:
            list = get_all_excluded_recette_ids_downstream(list,recette.recette)
        print(list)
        list.append(recette.id)
        return list
    else:
        print("HERE:"+str(list))
        print("HERE:"+recette.name)
        print("HERE:"+str(recette.id))
        list.append(recette.id)
        print("WILL RETURN:"+str(list))
        return list