from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..authentication import get_current_user
from ..dependencies import get_db
from ..schemas.recipes import CategoryRecipeResponseScheme, CategoryRecipeCreationScheme, RecipeCreationScheme
from ..schemas.users import UserResponseScheme
from ..models import CategoryRecipesModel, RecipesModel, RecipesIngredientsModel

router = APIRouter(
    prefix='/recipes',
    tags=['Recipes']
)


@router.get('/category/list', status_code=status.HTTP_200_OK, response_model=List[CategoryRecipeResponseScheme],
            summary='List of categories of recipes')
async def recipe_category_list(db: Session = Depends(get_db),
                               current_user: UserResponseScheme = Depends(get_current_user)):
    categories = db.query(CategoryRecipesModel).all()
    return categories


@router.get('/category/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryRecipeResponseScheme,
            summary='Get category by id')
async def get_recipe_category(category_id: int, db: Session = Depends(get_db),
                              current_user: UserResponseScheme = Depends(get_current_user)):
    category = db.query(CategoryRecipesModel).filter(CategoryRecipesModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    return category


@router.post('/category/create', status_code=status.HTTP_201_CREATED, response_model=CategoryRecipeResponseScheme,
             summary='Create a category for recipes')
async def create_recipe_category(category_scheme: CategoryRecipeCreationScheme, db: Session = Depends(get_db),
                                 current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    if db.query(CategoryRecipesModel).filter(CategoryRecipesModel.title == category_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Category already exists')
    category = CategoryRecipesModel(**category_scheme.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put('/category/update/{category_id}', status_code=status.HTTP_200_OK,
            response_model=CategoryRecipeResponseScheme, summary='Update category of recipes')
async def update_recipe_category(category_id: int, category_scheme: CategoryRecipeCreationScheme,
                                 db: Session = Depends(get_db),
                                 current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    category = db.query(CategoryRecipesModel).filter(CategoryRecipesModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    if db.query(CategoryRecipesModel).filter(CategoryRecipesModel.title == category_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Category already exists')
    category.title = category_scheme.title
    db.commit()
    db.refresh(category)
    return category


@router.delete('/category/delete/{category_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Delete a category of recipes')
async def delete_recipe_category(category_id, db: Session = Depends(get_db),
                                 current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    category = db.query(CategoryRecipesModel).filter(CategoryRecipesModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    db.delete(category)
    db.commit()


@router.post('/create', status_code=status.HTTP_201_CREATED, summary='Create a recipe',
             )
async def create_recipe(recipe_scheme: RecipeCreationScheme, db: Session = Depends(get_db),
                        current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    if db.query(RecipesModel).filter(RecipesModel.title == recipe_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Recipe already exists')
    recipe = RecipesModel(
        title=recipe_scheme.title,
        category_id=recipe_scheme.category_id,
        description=recipe_scheme.description,
        difficulty=recipe_scheme.difficulty
    )
    recipe.owner_id = current_user.id
    db.add(recipe)
    db.commit()
    recipe_ingredient = RecipesIngredientsModel()
    for value in recipe_scheme.ingredients:
        recipe_ingredient.recipe_id = recipe.id
        recipe_ingredient.ingredient_id = value.ingredient_id
        db.add(recipe_ingredient)
        db.commit()
        recipe_ingredient = RecipesIngredientsModel()
    db.refresh(recipe)
    return recipe


@router.get('/list', status_code=status.HTTP_200_OK, summary='List of recipes')
async def recipes_list(db: Session = Depends(get_db), current_user: UserResponseScheme = Depends(get_current_user)):
    recipes = db.query(RecipesModel, RecipesIngredientsModel.ingredient_id).join(RecipesIngredientsModel,
                                                                                 RecipesModel.id == RecipesIngredientsModel.recipe_id).all()
    return recipes


@router.get('/{recipe_id}', status_code=status.HTTP_200_OK, summary='Get recipe by id')
async def get_recipe(recipe_id: int, db: Session = Depends(get_db),
                     current_user: UserResponseScheme = Depends(get_current_user)):
    recipe = db.query(RecipesModel, RecipesIngredientsModel.ingredient_id).filter(RecipesModel.id == recipe_id).join(
        RecipesIngredientsModel,
        RecipesIngredientsModel.recipe_id == recipe_id).all()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Recipe not found')
    return recipe


@router.delete('/delete/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete a recipe')
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db),
                        current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    recipe = db.query(RecipesModel).filter(RecipesModel.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Recipe not found')
    ingredients = db.query(RecipesIngredientsModel).filter(RecipesIngredientsModel.recipe_id == recipe_id).all()
    db.delete(recipe)
    for value in ingredients:
        db.delete(value)
    db.commit()

