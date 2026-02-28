from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from schemas.schemas import CreateUser
from database.database import get_db
from sqlalchemy.orm import Session
from dependencies.security import hash_password

router = APIRouter(prefix='/bootstrap', tags=['Super-Admin'])

@router.post('/super-admin')
def create_super_admin(user_data: CreateUser, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.role == 'super_admin').first()

    if user:
        raise HTTPException(403, detail='Super-Admin already created! Route disabled.')
    
    user_data_dict = user_data.model_dump()
    user_data_dict['role'] = 'super_admin'
    user_data_dict['password'] = hash_password(user_data_dict['password'])
    super_admin = User(**user_data_dict)

    db.add(super_admin)
    db.commit()
    db.refresh(super_admin)

    return super_admin


    