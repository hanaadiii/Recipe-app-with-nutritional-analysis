from fastapi import APIRouter, Depends, Header, HTTPException
from typing import List
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

def get_current_user(username: str = Header(None)):
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username


class IngredientIn(BaseModel):
    name: str
    amount: float
    unit: str


class NutritionRequest(BaseModel):
    ingredients: List[IngredientIn]


@router.post("/analyze")
def analyze_nutrition(data: NutritionRequest, username=Depends(get_current_user)):

    total_cal = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0

    breakdown = []

    for ing in data.ingredients:
        nutr = scrape_nutrition_by_name(ing.name)

        factor = ing.amount / 100

        cal = nutr["calories"] * factor
        protein = nutr["proteins"] * factor
        fat = nutr["fats"] * factor
        carbs = nutr["carbs"] * factor

        breakdown.append({
            "ingredient": ing.name,
            "amount": ing.amount,
            "unit": ing.unit,
            "calories": cal,
            "proteins": protein,
            "fats": fat,
            "carbs": carbs
        })

        total_cal += cal
        total_protein += protein
        total_fat += fat
        total_carbs += carbs

    dominant = ["Protein", "Fat", "Carbs"][np.argmax(
        [total_protein, total_fat, total_carbs]
    )]

    return {
        "totals": {
            "calories": total_cal,
            "proteins": total_protein,
            "fats": total_fat,
            "carbs": total_carbs,
            "dominant_macro": dominant
        },
        "breakdown": breakdown
    }

