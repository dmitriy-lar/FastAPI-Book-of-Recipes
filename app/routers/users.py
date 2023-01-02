import os
from datetime import timedelta

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from ..dependencies import get_db
from ..schemas.users import UserCreationScheme, UserResponseScheme, Token
from ..models import UserModel
from ..authentication import get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, get_current_user

load_dotenv()

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/register', status_code=status.HTTP_200_OK, summary='Register User',
             response_model=UserResponseScheme)
async def register_user(user_scheme: UserCreationScheme, db: Session = Depends(get_db)):
    """
    You can register a new user
    """
    if db.query(UserModel).filter(UserModel.email == user_scheme.email).first():
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='User already exists')
    hashed_password = get_password_hash(user_scheme.password)
    user = UserModel(**user_scheme.dict())
    user.password = hashed_password
    if user_scheme.email == os.getenv('ADMIN_EMAIL') and user_scheme.password == os.getenv('ADMIN_PASSWORD'):
        user.is_admin = True
    else:
        user.is_admin = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserResponseScheme)
async def get_user(current_user: UserResponseScheme = Depends(get_current_user)):
    return current_user

