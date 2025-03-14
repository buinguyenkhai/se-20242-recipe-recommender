from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import models
from database import get_db

app = FastAPI()

# Import from json file
@app.post("/import_recipes/")
def import_recipes(db: Session = Depends(get_db)):
    # Danh sách các bảng cần xóa
    tables = ["recipe_tags", "steps", "recipe_ingredients", "ingredients", "tags", "recipes"]
    serial_table = {"recipes": "recipe_id", "ingredients": "ingredient_id", "tags": "tag_id"}

    # Kiểm tra và xóa dữ liệu nếu bảng tồn tại
    for table in tables:
        result = db.execute(text(f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{table}')")).scalar()
        print(result)
        if result:
            db.execute(text(f"DELETE FROM {table}"))
            if table in serial_table:
                db.execute(text(f"ALTER SEQUENCE {table}_{serial_table[table]}_seq RESTART WITH 1"))
    
    db.commit()
    with open("test.json", "r", encoding="utf-8") as f:
        recipes_data = json.load(f)

    #print(recipes_data)
    for recipe in recipes_data:
        new_recipe = models.Recipe(
            title=recipe["title"],
            image_url=recipe["image"],
            url=recipe["url"]
        )
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        for ingredient in recipe["ingredients"]:
            ing = db.query(models.Ingredient).filter(models.Ingredient.name == ingredient).first()
            if not ing:
                ing = models.Ingredient(name=ingredient)
                db.add(ing)
                db.commit()
                db.refresh(ing)

            recipe_ing = models.RecipeIngredient(
                recipe_id=new_recipe.recipe_id,
                ingredient_id=ing.ingredient_id,
                #quantity=ingredient["quantity"]
                quantity = None
            )
            db.add(recipe_ing)

        for i, (step_title, step_detail) in enumerate(zip(recipe["step-title"], recipe["step-detail"]), start=1):
            step = models.Step(
                recipe_id=new_recipe.recipe_id,
                step_number=i,
                step_title=step_title,
                step_detail=step_detail
            )
            db.add(step)


        if recipe["tags"] is None:
            recipe["tags"] = []

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

    return {"message": "Recipes imported successfully"}

# Lấy danh sách công thức
@app.get("/recipes/")
def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).all()
    return recipes

# Lấy chi tiết công thức theo ID
@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Lấy nguyên liệu và số lượng
    ingredients = db.query(models.RecipeIngredient).filter(models.RecipeIngredient.recipe_id == recipe_id).all()

    # Lấy các bước
    steps = db.query(models.Step).filter(models.Step.recipe_id == recipe_id).order_by(models.Step.step_number).all()

    # Lấy tags
    tags = db.query(models.RecipeTag).filter(models.RecipeTag.recipe_id == recipe_id).all()

    return {
        "title": recipe.title,
        "image_url": recipe.image_url,
        "url": recipe.url,
        "ingredients": [{"name": i.ingredient.name, "quantity": i.quantity} for i in ingredients],
        "steps": [{"step_number": s.step_number, "title": s.step_title, "detail": s.step_detail} for s in steps],
        "tags": [t.tag.tag_name for t in tags]
    }

# Thêm công thức mới
@app.post("/recipes/")
def create_recipe(recipe: dict, db: Session = Depends(get_db)):
    new_recipe = models.Recipe(title=recipe["title"], image_url=recipe["image_url"], url=recipe["url"])
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

# Xóa công thức
@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"message": "Recipe deleted"}

