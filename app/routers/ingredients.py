from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas.ingredients import CategoryIngredientScheme
from ..schemas.users import UserResponseScheme
from ..models import CategoryIngredientModel
from ..authentication import get_current_user

router = APIRouter(
    prefix='/ingredients',
    tags=['Ingredients']
)


@router.post('/category/create',
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryIngredientScheme,
             summary='Create a category for ingredients',
             response_description='Created category')
async def create_ingredient_category(
        category_scheme: CategoryIngredientScheme,
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
            response_model=List[CategoryIngredientScheme],
            summary='List of categories of ingredients',
            response_description='List of categories')
async def categories_list(db: Session = Depends(get_db)):
    """
    You will see the list of categories
    """
    categories = db.query(CategoryIngredientModel).all()
    return categories


@router.put('/category/update/{category_id}',
            status_code=status.HTTP_200_OK,
            response_model=CategoryIngredientScheme,
            summary='Update a category of ingredients',
            response_description='Updated category')
async def update_category(
        category_id: int,
        category_scheme: CategoryIngredientScheme,
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
            response_model=CategoryIngredientScheme,
            status_code=status.HTTP_200_OK,
            summary='Get category by id')
async def get_category(
        category_id: int,
        db: Session = Depends(get_db)):
    """
    To get a category you need to pass _category_id_
    """
    category = db.query(CategoryIngredientModel).filter(CategoryIngredientModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category was not found')
    return category
