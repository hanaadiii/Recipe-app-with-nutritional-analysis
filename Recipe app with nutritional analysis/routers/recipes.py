from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from models.shemas import RecipeCreate, RecipeOut, IngredientOut
from database.database import get_db
from auth import require_api_key


router = APIRouter(prefix="/recipes", tags=["Recipes"])

def get_current_user(username: str = Header(None)):
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username


@router.get("/", response_model=List[RecipeOut])
def list_recipes():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM recipes")
    recipes = []

    for r in cur.fetchall():
        rec = dict(r)

        cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (rec["id"],))
        ingredients = [IngredientOut(**dict(i)) for i in cur.fetchall()]

        recipes.append({
            "id": rec["id"],
            "owner": rec["owner"],
            "title": rec["title"],
            "description": rec["description"],
            "ingredients": ingredients
        })

    return recipes


@router.post("/", response_model=RecipeOut)
def create_recipe(payload: RecipeCreate, username=Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO recipes (owner, title, description) VALUES (?, ?, ?)",
                (username, payload.title, payload.description))
    recipe_id = cur.lastrowid

    for ing in payload.ingredients:
        cur.execute(
            "INSERT INTO ingredients (recipe_id, name, amount, unit) VALUES (?, ?, ?, ?)",
            (recipe_id, ing.name, ing.amount, ing.unit)
        )

    conn.commit()

    cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    r = dict(cur.fetchone())

    cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    ingredients = [IngredientOut(**dict(i)) for i in cur.fetchall()]

    return {
        "id": r["id"],
        "owner": r["owner"],
        "title": r["title"],
        "description": r["description"],
        "ingredients": ingredients
    }


    conn.close()
    return recipes


@router.post("/", response_model=RecipeOut, dependencies=[Depends(require_api_key)])
def create_recipe(payload: RecipeCreate, user=Depends(require_api_key)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO recipes(owner_id, title, description) VALUES (?, ?, ?)",
        (user["id"], payload.title, payload.description)
    )
    recipe_id = cur.lastrowid

    for ing in payload.ingredients:
        cur.execute(
            "INSERT INTO ingredients(recipe_id, name, amount, unit, calories) VALUES (?,?,?,?,?)",
            (recipe_id, ing.name, ing.amount, ing.unit, ing.calories)
        )

    conn.commit()

    cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    r = dict(cur.fetchone())

    cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    ingredients = [IngredientOut(**dict(i)) for i in cur.fetchall()]

    conn.close()

    return {
        "id": recipe_id,
        "owner_id": r["owner_id"],
        "title": r["title"],
        "description": r["description"],
        "ingredients": ingredients
    }


@router.get("/mine", response_model=List[RecipeOut], dependencies=[Depends(require_api_key)])
def my_recipes(user=Depends(require_api_key)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM recipes WHERE owner_id = ?", (user["id"],))
    rows = cur.fetchall()
    recipes = []

    for r in rows:
        rec = dict(r)

        cur.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (rec["id"],))
        ingredients = [IngredientOut(**dict(i)) for i in cur.fetchall()]

        recipes.append({
            "id": rec["id"],
            "owner_id": rec["owner_id"],
            "title": rec["title"],
            "description": rec["description"],
            "ingredients": ingredients
        })

    conn.close()
    return recipes

