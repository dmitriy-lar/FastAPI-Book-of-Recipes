from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas.ingredients import CategoryIngredientCreationScheme, IngredientCreationScheme, \
    CategoryIngredientResponseScheme, IngredientResponseScheme
from ..schemas.users import UserResponseScheme
from ..models import CategoryIngredientModel, IngredientModel
from ..authentication import get_current_user

router = APIRouter(
    prefix='/ingredients',
    tags=['Ingredients']
)


@router.post('/category/create',
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryIngredientCreationScheme,
             summary='Create a category for ingredients',
             response_description='Created category')
async def create_ingredient_category(
        category_scheme: CategoryIngredientCreationScheme,
        db: Session = Depends(get_db),
        current_user: UserResponseScheme = Depends(get_current_user)):
    """
    You can create a category with two parameters:
    - _title_ (Name of the category)
    - _description_ (It is not a required parameter. You can leave it blank)
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    if db.query(CategoryIngredientModel).filter(CategoryIngredientModel.title == category_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='This category already exists')
    category = CategoryIngredientModel(**category_scheme.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get('/category/list',
            status_code=status.HTTP_200_OK,
            response_model=List[CategoryIngredientResponseScheme],
            summary='List of categories of ingredients',
            response_description='List of categories')
async def categories_list(db: Session = Depends(get_db), current_user: UserResponseScheme = Depends(get_current_user)):
    """
    You will see the list of categories
    """
    categories = db.query(CategoryIngredientModel).all()
    return categories


@router.put('/category/update/{category_id}',
            status_code=status.HTTP_200_OK,
            response_model=CategoryIngredientCreationScheme,
            summary='Update a category of ingredients',
            response_description='Updated category')
async def update_category(
        category_id: int,
        category_scheme: CategoryIngredientCreationScheme,
        db: Session = Depends(get_db),
        current_user: UserResponseScheme = Depends(get_current_user)):
    """
    To update a category you need to pass _category_id_
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    category = db.query(CategoryIngredientModel).filter(CategoryIngredientModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    if db.query(CategoryIngredientModel).filter(CategoryIngredientModel.title == category_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Category already exists')
    category.title = category_scheme.title
    category.description = category_scheme.description

    db.commit()
    db.refresh(category)
    return category


@router.delete('/category/delete/{category_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               summary='Delete a category')
async def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponseScheme = Depends(get_current_user)):
    """
    To delete a category you need to pass _category_id_
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    category = db.query(CategoryIngredientModel).filter(CategoryIngredientModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    db.delete(category)
    db.commit()


@router.get('/category/{category_id}',
            response_model=CategoryIngredientResponseScheme,
            status_code=status.HTTP_200_OK,
            summary='Get category by id')
async def get_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: UserResponseScheme = Depends(get_current_user)):
    """
    To get a category you need to pass _category_id_
    """
    category = db.query(CategoryIngredientModel).filter(CategoryIngredientModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    return category


@router.post('/create',
             status_code=status.HTTP_201_CREATED,
             summary='Create an ingredient',
             response_model=IngredientCreationScheme,
             description=f"You can create an ingredient here.")
async def create_ingredient(ingredient_scheme: IngredientCreationScheme,
                            db: Session = Depends(get_db),
                            current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    if db.query(CategoryIngredientModel).filter(
            CategoryIngredientModel.id == ingredient_scheme.category_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')

    if db.query(IngredientModel).filter(IngredientModel.title == ingredient_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Ingredient already exists')

    ingredient = IngredientModel(**ingredient_scheme.dict())
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.get('/list',
            status_code=status.HTTP_200_OK,
            summary='List of ingredients',
            response_model=List[IngredientResponseScheme]
            )
async def ingredient_list(db: Session = Depends(get_db), current_user: UserResponseScheme = Depends(get_current_user)):
    ingredients = db.query(IngredientModel).all()
    return ingredients


@router.put('/update/{ingredient_id}',
            status_code=status.HTTP_200_OK,
            summary='Update an ingredient',
            )
async def update_ingredient(
        ingredient_id: int,
        ingredient_scheme: IngredientCreationScheme,
        db: Session = Depends(get_db), current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ingredient was not found')
    if db.query(IngredientModel).filter(IngredientModel.title == ingredient_scheme.title).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Ingredient already exists')
    ingredient.title = ingredient_scheme.title
    ingredient.category_id = ingredient_scheme.category_id
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.delete('/delete/{ingredient_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete an ingredient')
async def delete_ingredient(ingredient_id, db: Session = Depends(get_db),
                            current_user: UserResponseScheme = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have enough permissions')
    ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ingredient was not found')
    db.delete(ingredient)
    db.commit()


@router.get('/{ingredient_id}', response_model=IngredientCreationScheme, status_code=status.HTTP_200_OK,
            summary='Get ingredient by id')
async def get_ingredient(ingredient_id, db: Session = Depends(get_db),
                         current_user: UserResponseScheme = Depends(get_current_user)):
    ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ingredient was not found')
    return ingredient
