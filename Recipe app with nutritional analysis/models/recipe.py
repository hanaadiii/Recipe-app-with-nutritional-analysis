from pydantic import BaseModel
from typing import List
from ingredient import IngredientOut


class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]

class RecipeOut(BaseModel):
    id: int
    title: str
