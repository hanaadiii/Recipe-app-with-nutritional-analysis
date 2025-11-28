CALORIE_DATABASE = {
    "banana": 0.89,
    "apple": 0.52,
    "bread": 2.65,
    "egg": 1.55,
    "milk": 0.42,
    "rice": 1.30,
    "chicken": 2.39,
    "butter": 7.17
}

def analyze_ingredient(ingredient: str, quantity: float):
    ingredient = ingredient.lower().strip()

    if ingredient not in CALORIE_DATABASE:
        return {
            "ingredient": ingredient,
            "quantity": quantity,
            "calories": None,
            "error": "Ingredient not found in database"
        }

    calories = CALORIE_DATABASE[ingredient] * quantity

    return {
        "ingredient": ingredient,
        "quantity": quantity,
        "calories": round(calories, 2)
    }

