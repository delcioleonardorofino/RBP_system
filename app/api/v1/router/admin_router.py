from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schemas import UserOut, CreateUser, CreateTurma
from models.models import User, Turma
from services.school_services import get_school_name
from dependencies.security import get_current_user, hash_password

router = APIRouter(prefix='/admin', tags=['admin'])


# @router.get('/me', response_model=UserOut)
# def get_profile(current_user: User = Depends(get_current_user), 
#                 db: Session = Depends(get_db)):
    
#     if current_user.role in ['super_admin', 'studend']:
#         raise HTTPException(403, detail='Operation not permitted!')

#     profile_info = db.query(User).filter(User.id == current_user.id).first()
#     if not profile_info:
#         raise HTTPException(404, detail='User not found!')
    
#     return profile_info


# Secretaria

@router.get('/secretaria', response_model=list[UserOut])
def get_all_users_of_school(
                            current_user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    users = db.query(User).filter(User.school_id == current_user.school_id, User.role == 'secretaria').all()

    if not users:
        raise HTTPException(404, detail='No users found!')

    return get_school_name(db, users)

@router.get('/secretaria/{user_id}', response_model=UserOut)
def get_secretary_agent(user_id:int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    user = db.query(User).filter(User.id == user_id, User.school_id == current_user.school_id, User.role == 'secretaria').first()

    if not user:
        raise HTTPException(404, detail='User not found!')

    return user

@router.post('/secretaria')
def create_secretary_agent(
                        user_data: CreateUser, 
                        current_user: User = Depends(get_current_user), 
                        db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    new_user = User(**user_data.model_dump())
    new_user.role = 'secretaria'
    new_user.school_id = current_user.school_id
    new_user.password = hash_password(new_user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

# Teachers

@router.get('/teachers', response_model=list[UserOut])
def get_all_teachers_of_school(
                            current_user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    users = db.query(User).filter(User.school_id == current_user.school_id, User.role == 'teacher').all()

    if not users:
        raise HTTPException(404, detail='No users found!')
    


    return users

@router.get('/teachers/{user_id}', response_model=UserOut)
def get_teacher_by_id(user_id:int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    user = db.query(User).filter(User.id == user_id, User.school_id == current_user.school_id, User.role == 'teacher').first()

    if not user:
        raise HTTPException(404, detail='User not found!')

    return user

@router.post('/teachers')
def create_teacher(
                        user_data: CreateUser, 
                        current_user: User = Depends(get_current_user), 
                        db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    new_user = User(**user_data.model_dump())
    new_user.school_id = current_user.school_id
    new_user.role = 'professor'
    new_user.password = hash_password(new_user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

# Turmas

# Add response schema as a ClassOut
@router.get('/turmas')
def get_all_classes_of_school(
                            current_user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    turmas = db.query(Turma).filter(Turma.school_id == current_user.school_id).all()

    if not turmas:
        raise HTTPException(404, detail='No classes found!')

    return turmas

@router.get('/turmas/{turma_id}')
def get_turma_by_id(turma_id:int,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    turma = db.query(Turma).filter(Turma.id == turma_id, Turma.school_id == current_user.school_id).first()

    if not turma:
        raise HTTPException(404, detail='Class not found!')

    return turma

@router.post('/turmas')
def create_turma(turma_data: CreateTurma, 
                current_user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)):

    if current_user.role != 'admin_escola':
        raise HTTPException(403, detail='Operation not permitted!')
    
    new_turma = Turma(**turma_data.model_dump())
    new_turma.school_id = current_user.school_id

    db.add(new_turma)
    db.commit()
    db.refresh(new_turma)    
    return new_turma