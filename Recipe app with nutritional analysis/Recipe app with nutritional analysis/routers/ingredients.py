from fastapi import APIRouter, Depends
from typing import List
from database.database import get_connection
from models.shemas import IngredientCreate, IngredientOut
from auth import require_api_key

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.get("/", response_model=List[IngredientOut])
def list_ingredients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ingredients")
    rows = cur.fetchall()
    ingredients = [IngredientOut(**dict(r)) for r in rows]
    conn.close()
    return ingredients

@router.post("/", response_model=IngredientOut, dependencies=[Depends(require_api_key)])
def add_ingredient(ingredient: IngredientCreate, user=Depends(require_api_key)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ingredients(recipe_id, name, amount, unit, calories) VALUES (?,?,?,?,?)",
        (0, ingredient.name, ingredient.amount, ingredient.unit, ingredient.calories)
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.execute("SELECT * FROM ingredients WHERE id = ?", (new_id,))
    row = dict(cur.fetchone())
    conn.close()
    return IngredientOut(**row)
