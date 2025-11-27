from fastapi import FastAPI
from database.database import init_db
from routers.users import router as users_router
from routers.recipes import router as recipes_router
from routers.ingredients import router as ingredients_router
from routers.nutrition import router as nutrition_router

app = FastAPI(title="Recipe App with Nutritional Analysis")

init_db()

app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(ingredients_router)
app.include_router(nutrition_router)

@app.get("/")
def root():
    return {"msg": "Recipe app backend running"}

