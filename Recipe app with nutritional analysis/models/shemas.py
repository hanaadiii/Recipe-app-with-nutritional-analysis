from pydantic import BaseModel, Field
from typing import Optional, List

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str

class TokenOut(BaseModel):
    api_key: str

class IngredientCreate(BaseModel):
    name: str
    amount: float
    unit: Optional[str] = None
    calories: Optional[float] = 0.0

class IngredientOut(BaseModel):
    id: int
    recipe_id: int
    name: str
    amount: float
    unit: Optional[str] = None
    calories: float

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[IngredientCreate] = []

class RecipeOut(BaseModel):
    id: int
    owner_id: int
    title: str
    description: Optional[str] = None
    ingredients: List[IngredientOut] = []
