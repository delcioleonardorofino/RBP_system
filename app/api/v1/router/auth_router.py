from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.schemas import CreateUser, UserOut
from dependencies.security import oauth2_scheme
from services.auth_services import login_user, logout_user, get_current_user
from services.school_services import get_school_name
from models.models import User
from sqlalchemy.orm import Session
from database.database import get_db

router = APIRouter(prefix='/auth', tags=['auth'])

# @router.post('/signup')
# def signup(user_data: CreateUser, 
#            current_user: User = Depends(get_current_user), 
#            db: Session = Depends(get_db)):
    
#     print('Debug Current User:', current_user)
#     return create_user(db, user_data, current_user)

@router.get('/me', response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    
    return get_school_name(db, current_user)

@router.post('/login')
def login(login_form : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    return login_user(db, login_form)

@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
   
    return logout_user(db, token)


        