
from dependencies.security import (verify_hash,
                                create_access_token, 
                                hash_password, 
                                oauth2_scheme, 
                                get_current_user)
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from schemas.schemas import TokenSchema, CreateUser
from models.models import User, RevokedToken
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from configs import SECRET_KEY, ALGORITHM


def create_user(db: Session, 
                user_data: CreateUser, 
                current_user: User):
    print(current_user.role)
    
    if current_user.role == 'super_admin':
        if user_data.role != 'super_admin' and user_data.role in ['admin_escola', 'secretaria', 'professor', 'director']:
            role = user_data.role
        else:
           raise HTTPException(403, detail='Not Allowed to create such user!') 
    
    elif current_user.role == 'admin_escola':
        if user_data.role in ['admin_escola', 'super_admin'] or user_data.role not in ['secretaria', 'director', 'professor']:
            raise HTTPException(403, 'Not allowed to create such users!')
        else:
            role = user_data.role
    
    else:
        raise HTTPException(403, detail='Operation not permitted!')
        
    
    user = db.query(User).filter(User.email == user_data.email).first()

    if user:
        return {'message': 'User already exists!',
                'field': 'email'}
    
    user_data.password = hash_password(user_data.password)
    user_data.role = role

    new_user = User(**user_data.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user( db: Session, login_form: OAuth2PasswordRequestForm = Depends()):


    user = db.query(User).filter(User.email == login_form.username).first()

    if not user or not verify_hash(login_form.password, user.password):
        raise HTTPException(403, detail='Wrong credentials or user does not exist!')
    
    print(user.id)

    token_payload = TokenSchema(
        sub = str(user.id),
        role = user.role,
        )

    token_payload_dict = token_payload.model_dump()

    print(token_payload_dict)

    token = create_access_token(token_payload_dict)

            # print(token)

    return {'access_token': token, 'type': 'bearer'}

def logout_user( db: Session, token: str = Depends(oauth2_scheme)):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    jti = payload.get('jti')

    db.add(RevokedToken(jti=jti))
    db.commit()

    return {'detail':'Logout successfull'}

