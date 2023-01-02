from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from ..dependencies import get_db
from ..schemas.users import UserCreationScheme, UserResponseScheme
from ..models import UserModel
from ..authentication import get_password_hash, verify_password

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
