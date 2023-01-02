import sqlalchemy
from sqlalchemy.orm import relationship

from .databases import Base


class CategoryIngredientModel(Base):
    __tablename__ = 'category_ingredients'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    ingredients = relationship('IngredientModel', back_populates='category')

    def __str__(self):
        return self.title


class IngredientModel(Base):
    __tablename__ = 'ingredients'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
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
