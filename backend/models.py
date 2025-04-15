from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    image_url = Column(String)
    url = Column(String)
    source_id = Column(Integer, ForeignKey("sources.source_id"))  # Liên kết với Source

    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    steps = relationship("Step", back_populates="recipe")
    tags = relationship("RecipeTag", back_populates="recipe")
    source = relationship("Source", back_populates="recipes")  # Quan hệ với Source


class Source(Base):
    __tablename__ = "sources"

    source_id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, unique=True, nullable=False)

    recipes = relationship("Recipe", back_populates="source")  # Liên kết với Recipe


class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship("RecipeIngredient", back_populates="ingredient")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id"), primary_key=True)
    quantity = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")


class Step(Base):
    __tablename__ = "steps"

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    step_number = Column(Integer, primary_key=True)
    step_detail = Column(String, nullable=False)  # Chỉ giữ lại step_detail

    recipe = relationship("Recipe", back_populates="steps")


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String)

    recipes = relationship("RecipeTag", back_populates="tag")


class RecipeTag(Base):
    __tablename__ = "recipe_tags"

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id"), primary_key=True)

    recipe = relationship("Recipe", back_populates="tags")
    tag = relationship("Tag", back_populates="recipes")
