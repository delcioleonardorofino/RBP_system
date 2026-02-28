from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.models import User, RevokedToken
from jose import jwt, JWTError
from database.database import get_db
from datetime import datetime, timedelta
from configs import ALGORITHM, SECRET_KEY, TOKEN_EXPIRE_TIME
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

def hash_password(plain_password: str) -> str:
    
    password_hash: str = pwd_context.hash(plain_password)
    return password_hash

def verify_hash(plain_password: str, password_hash: str) -> bool:

    return pwd_context.verify(plain_password, password_hash)

def create_access_token(data: dict) -> str:

    payload = data.copy()

    jti = str(uuid.uuid4())
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_TIME)
    payload.update({'exp': expiration, 'jti':jti})
    print(payload)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)):
    print(token)

    # try:
    #     print(f"DEBUG: Tentando decodificar o token: {token[:10]}...") 
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     print(f"DEBUG: Payload: {payload}")
    # except Exception as e:
    #     print(f"ERRO CRÍTICO NA DECODIFICAÇÃO: {type(e).__name__} - {e}")
    #     raise HTTPException(status_code=401, detail=str(e))
    
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id = int(payload.get('sub'))
        jti = payload.get('jti')

        if not user_id or not jti:
            print('no user id or jti')
            raise HTTPException(401, detail='Invalid Token!')

    except JWTError:
        print('jwt error')
        raise HTTPException(401, detail='Invalid Token!')
    
    if db.query(RevokedToken).filter(RevokedToken.jti == jti).first():
        print('token revoked')
        raise HTTPException(401, detail='Token has been revoked!')
    
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        print('no user')
        raise HTTPException(401, detail='User not found!') 
    
    return current_user
    