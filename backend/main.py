from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import json
import models
from database import get_db, Base, engine
import uvicorn
import re
import unicodedata

def preprocess_vietnamese(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    stopwords = {
       "và", "là", "của", "có", "cho", "trên", "với", "ở", "những", "các", "một", "được", "này"
    }

    tokens = text.split()
    filtered = [t for t in tokens if t not in stopwords]
    return ' '.join(filtered)


Base.metadata.create_all(bind=engine)

app = FastAPI()

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent;"))
    conn.commit()

# Check server status
@app.get("/health")
def health():
    return {"status": "ok"}

# Import from json file
@app.post("/import_recipes/")
def import_recipes(db: Session = Depends(get_db)):
    # Danh sách các bảng cần xóa
    tables = ["recipe_tags", "steps", "recipe_ingredients", "ingredients", "tags", "recipes", "sources"]
    serial_table = {"recipes": "recipe_id", "ingredients": "ingredient_id", "tags": "tag_id", "sources": "source_id"}

    # Kiểm tra và xóa dữ liệu nếu bảng tồn tại
    for table in tables:
        result = db.execute(text(f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{table}')")).scalar()
        if result:
            db.execute(text(f"DELETE FROM {table}"))
            if table in serial_table:
                db.execute(text(f"ALTER SEQUENCE {table}_{serial_table[table]}_seq RESTART WITH 1"))
    
    db.commit()

    with open("vaobep.json", "r", encoding="utf-8") as f:
        recipes_data = json.load(f)

    for recipe in recipes_data:
        # Xử lý nguồn (Source)
        source_name = recipe.get("source", "Unknown")
        source = db.query(models.Source).filter(models.Source.source_name == source_name).first()
        if not source:
            source = models.Source(source_name=source_name)
            db.add(source)
            db.commit()
            db.refresh(source)

        # Tạo Recipe mới
        new_recipe = models.Recipe(
            title=recipe["title"],
            image_url=recipe["image"],
            url=recipe["url"],
            source_id=source.source_id
        )
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        # Thêm Ingredients
        for ingredient_name in recipe["ingredients"]:
            ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient_name).first()
            if not ingredient:
                ingredient = models.Ingredient(name=ingredient_name)
                db.add(ingredient)
                db.commit()
                db.refresh(ingredient)

            recipe_ing = models.RecipeIngredient(
                recipe_id=new_recipe.recipe_id,
                ingredient_id=ingredient.ingredient_id,
                quantity=None  # Không có thông tin số lượng
            )
            db.add(recipe_ing)

        # Thêm Steps (chỉ có step_detail)
        steps = recipe.get("step-detail", "").split("\n")  # Tách thành từng bước
        for i, step_detail in enumerate(steps, start=1):
            step = models.Step(
                recipe_id=new_recipe.recipe_id,
                step_number=i,
                step_detail=step_detail.strip()
            )
            db.add(step)

        # Thêm Tags
        tags = recipe.get("tags", []) or []  # Đảm bảo không bị lỗi nếu None
        for tag_name in tags:
            tag = db.query(models.Tag).filter(models.Tag.tag_name == tag_name).first()
            if not tag:
                tag = models.Tag(tag_name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)

            recipe_tag = models.RecipeTag(
                recipe_id=new_recipe.recipe_id,
                tag_id=tag.tag_id
            )
            db.add(recipe_tag)

        db.commit()

    return {"message": "Recipes imported successfully"}

# API lấy tất cả recipes
@app.get("/recipes/")
def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).all()
    return recipes

# API lấy một recipe theo ID
@app.get("/recipes/{recipe_id}/")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# API lấy tất cả ingredients
@app.get("/ingredients/")
def get_ingredients(db: Session = Depends(get_db)):
    ingredients = db.query(models.Ingredient).all()
    return ingredients

# API lấy một ingredient theo ID
@app.get("/ingredients/{ingredient_id}/")
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(models.Ingredient).filter(models.Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

# API lấy tất cả tags
@app.get("/tags/")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    return tags

# API lấy một tag theo ID
@app.get("/tags/{tag_id}/")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# API nâng cao: Lấy danh sách nguyên liệu theo recipe_id
@app.get("/recipes/{recipe_id}/ingredients/")
def get_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    ingredients = (
        db.query(models.Ingredient)
        .join(models.RecipeIngredient, models.Ingredient.ingredient_id == models.RecipeIngredient.ingredient_id)
        .filter(models.RecipeIngredient.recipe_id == recipe_id)
        .all()
    )
    if not ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found for this recipe")
    return ingredients

# API nâng cao: Lấy danh sách bước làm theo recipe_id
@app.get("/recipes/{recipe_id}/steps/")
def get_recipe_steps(recipe_id: int, db: Session = Depends(get_db)):
    steps = db.query(models.Step).filter(models.Step.recipe_id == recipe_id).order_by(models.Step.step_number).all()
    if not steps:
        raise HTTPException(status_code=404, detail="No steps found for this recipe")
    return steps

# API nâng cao: Lấy danh sách tags theo recipe_id
@app.get("/recipes/{recipe_id}/tags/")
def get_recipe_tags(recipe_id: int, db: Session = Depends(get_db)):
    tags = (
        db.query(models.Tag)
        .join(models.RecipeTag, models.Tag.tag_id == models.RecipeTag.tag_id)
        .filter(models.RecipeTag.recipe_id == recipe_id)
        .all()
    )
    if not tags:
        raise HTTPException(status_code=404, detail="No tags found for this recipe")
    return tags

@app.get("/recipes/by_ingredient/{ingredient_name}/")
def get_recipes_by_ingredient(ingredient_name: str, db: Session = Depends(get_db)):
    # Tìm tất cả nguyên liệu có tên chứa từ khóa
    ingredients = db.query(models.Ingredient).filter(
        func.unaccent(func.lower(models.Ingredient.name)).ilike(f"%{ingredient_name.lower()}%")
    ).all()

    if not ingredients:
        raise HTTPException(status_code=404, detail="No matching ingredients found")

    ingredient_ids = [i.ingredient_id for i in ingredients]

    # Tìm tất cả các công thức có chứa các nguyên liệu trên
    recipe_ids = db.query(models.RecipeIngredient.recipe_id).filter(
        models.RecipeIngredient.ingredient_id.in_(ingredient_ids)
    ).distinct()

    recipes = db.query(models.Recipe).filter(
        models.Recipe.recipe_id.in_(recipe_ids)
    ).all()

    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found for these ingredients")

    return recipes

@app.post("/add_ingredient/")
def add_ingredient(name: str, db: Session = Depends(get_db)):
    existing_ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == name).first()
    if existing_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient already exists")

    new_ingredient = models.Ingredient(name=name)
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return {"message": "Ingredient added successfully", "ingredient_id": new_ingredient.ingredient_id}

@app.post("/add_recipe/")
def add_recipe(recipe: dict, db: Session = Depends(get_db)):
    # Tạo công thức mới
    new_recipe = models.Recipe(
        title=recipe["title"],
        image_url=recipe["image_url"],
        url=recipe["url"]
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Thêm nguyên liệu
    for ingredient_name in recipe["ingredients"]:
        ingredient = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient_name).first()
        if not ingredient:
            ingredient = models.Ingredient(name=ingredient_name)
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)

        recipe_ing = models.RecipeIngredient(
            recipe_id=new_recipe.recipe_id,
            ingredient_id=ingredient.ingredient_id
        )
        db.add(recipe_ing)

    # Thêm bước thực hiện
    for i, step in enumerate(recipe["steps"], start=1):
        new_step = models.Step(
            recipe_id=new_recipe.recipe_id,
            step_number=i,
            step_title=step["title"],
            step_detail=step["detail"]
        )
        db.add(new_step)

    # Thêm tags
    for tag_name in recipe["tags"]:
        tag = db.query(models.Tag).filter(models.Tag.tag_name == tag_name).first()
        if not tag:
            tag = models.Tag(tag_name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        recipe_tag = models.RecipeTag(
            recipe_id=new_recipe.recipe_id,
            tag_id=tag.tag_id
        )
        db.add(recipe_tag)

    db.commit()
    return {"message": "Recipe added successfully", "recipe_id": new_recipe.recipe_id}

@app.get("/search/")
def search_recipes(
    query: str = Query(...),
    db: Session = Depends(get_db)
):
    processed_query = preprocess_vietnamese(query)
    ts_query = func.websearch_to_tsquery('simple', processed_query)
    #ts_query = func.plainto_tsquery('simple', processed_query)

    search = (
        db.query(models.Recipe)
        .outerjoin(models.Recipe.ingredients)
        .outerjoin(models.Ingredient)
        .outerjoin(models.Recipe.tags)
        .outerjoin(models.Tag)
        .filter(
            func.to_tsvector('simple', func.coalesce(models.Recipe.title, '')).op('@@')(ts_query)
            |
            func.to_tsvector('simple', func.coalesce(models.Ingredient.name, '')).op('@@')(ts_query)
            |
            func.to_tsvector('simple', func.coalesce(models.Tag.tag_name, '')).op('@@')(ts_query)
        )
        .distinct()
    )

    recipes = search.all()

    return [
        {
            "recipe_id": r.recipe_id,
            "title": r.title,
            "image_url": r.image_url,
            "url": r.url,
        }
        for r in recipes
    ]




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)