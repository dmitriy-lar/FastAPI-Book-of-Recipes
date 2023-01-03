import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .databases import Base


class CategoryIngredientModel(Base):
    __tablename__ = 'category_ingredients'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    ingredients = relationship('IngredientModel', back_populates='category')

    def __str__(self):
        return self.title


class RecipesIngredientsModel(Base):
    __tablename__ = 'recipes_ingredient'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    recipe_id = sqlalchemy.Column(sqlalchemy.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = sqlalchemy.Column(sqlalchemy.ForeignKey('ingredients.id'), nullable=False)


class IngredientModel(Base):
    __tablename__ = 'ingredients'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('category_ingredients.id'))
    category = relationship('CategoryIngredientModel', back_populates='ingredients')

    def __str__(self):
        return self.title


class UserModel(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    def __str__(self):
        return self.email


class CategoryRecipesModel(Base):
    __tablename__ = 'category_recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    recipes = relationship('RecipesModel', backref='category')

    def __str__(self):
        return self.title


class RecipesModel(Base):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    category_id = sqlalchemy.Column(sqlalchemy.ForeignKey('category_recipes.id'), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), server_default=func.now())
    owner_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'), nullable=False)
    difficulty = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    ingredients = relationship('IngredientModel', secondary='recipes_ingredient', backref='recipes', lazy=True)
    owner = relationship('UserModel', backref='recipes')

    def __str__(self):
        return self.title
