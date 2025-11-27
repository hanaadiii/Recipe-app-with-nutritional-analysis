from pydantic import BaseModel

class IngredientIn(BaseModel):
    name: str
    amount: float

class IngredientOut(BaseModel):
    id: int
    name: str
    amount: float
