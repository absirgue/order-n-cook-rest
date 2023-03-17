# This file is bound to be refactored. Will hold all helper functions until refactoring becomes a need.

# Return the conversion rate from an ingredient to a unit to kilogramme.
from core_routes.models import Conversions, Ingredients


def get_conversion_rate(ingredientId, unit):
    try:
        ingredient = Ingredients.objects.get(id=ingredientId)
        if unit == "kilogramme":
            return 1
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