import numpy as np
from typing import List, Dict

def scale_nutrition_per_amount(nut_per_100g: Dict[str, float], amount_g: float) -> Dict[str, float]:

    factor = amount_g / 100.0
    return {
        "calories": nut_per_100g.get("calories", 0.0) * factor,
        "proteins": nut_per_100g.get("proteins", 0.0) * factor,
        "fats": nut_per_100g.get("fats", 0.0) * factor,
        "carbs": nut_per_100g.get("carbs", 0.0) * factor,
    }

def analyze_ingredients(ingredients: List[Dict]) -> Dict:

    total_cal = 0.0
    total_prot = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    breakdown = []

    for ing in ingredients:
        name = ing.get("name")
        amount = float(ing.get("amount", 0.0))
        nut100 = ing.get("nutrition_per_100g", {"calories":0, "proteins":0, "fats":0, "carbs":0})
        scaled = scale_nutrition_per_amount(nut100, amount)

        total_cal += scaled["calories"]
        total_prot += scaled["proteins"]
        total_fat += scaled["fats"]
        total_carbs += scaled["carbs"]

        breakdown.append({
            "name": name,
            "amount": amount,
            "calories": scaled["calories"],
            "proteins": scaled["proteins"],
            "fats": scaled["fats"],
            "carbs": scaled["carbs"],
        })

    arr = np.array([[b["proteins"], b["fats"], b["carbs"]] for b in breakdown], dtype=float)
    macro_sums = arr.sum(axis=0) if arr.size else np.array([0.0,0.0,0.0])
    protein_total, fat_total, carbs_total = macro_sums.tolist()

    profile = "balanced"
    if protein_total > fat_total + carbs_total:
        profile = "high protein"
    elif fat_total > protein_total + carbs_total:
        profile = "high fat"
    elif carbs_total > protein_total + fat_total:
        profile = "high carbs"

    totals = {
        "calories": total_cal,
        "proteins": total_prot,
        "fats": total_fat,
        "carbs": total_carbs,
    }

    return {
        "totals": totals,
        "breakdown": breakdown,
        "macro_sums": {"proteins": protein_total, "fats": fat_total, "carbs": carbs_total},
        "profile": profile
    }
