from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils.nutrition import analyze_ingredient

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

class IngredientInput(BaseModel):
    name: str
    amount: float
    unit: str = "g"

class IngredientList(BaseModel):
    ingredients: List[IngredientInput]

@router.post("/analyze")
def analyze(payload: IngredientList):
    results = []
    total_calories = 0

    for ing in payload.ingredients:
        result = analyze_ingredient(ing.name, ing.amount)
        results.append(result)

        if result["calories"] is not None:
            total_calories += result["calories"]

    return {
        "totals": {"calories": round(total_calories, 2)},
        "breakdown": results
    }

