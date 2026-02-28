from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schemas import CreateSchool, CreateUser, SchoolOut
from models.models import School, User
from services.school_services import get_school_name
from dependencies.security import get_current_user, hash_password

router = APIRouter( tags=['Super-Admin'])


@router.post('/create-school')
def create_school_tenant(school_data: CreateSchool, 
                         current_user: User = Depends(get_current_user), 
                         db: Session = Depends(get_db)):
    if current_user.role != 'super_admin':
        raise HTTPException(403, detail='Operation not permitted!')
    
    new_school = School(**school_data.model_dump())
    new_school.user_id = current_user.id

    db.add(new_school)
    db.commit()
    db.refresh(new_school)

    return new_school

@router.get('/schools', response_model=list[SchoolOut])
def get_schools(current_user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    if current_user.role != 'super_admin':
        raise HTTPException(403, detail='Operation not permitted!')
    
    schools = db.query(School).all()
    
    return schools

@router.post('/{school_id}/school-admin')
def create_school_admin(school_id: int, 
                        user_data: CreateUser, 
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    
    if current_user.role != 'super_admin':
        raise HTTPException(403, detail='Operation not permitted!')

    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(404, detail='School not found!')

    admin = db.query(User).filter(User.role == 'admin_escola', User.school_id == school_id).first()
    if admin:

        raise HTTPException(403, detail='School Admin already exists for this school!')

    school_admin = User(**user_data.model_dump())
    school_admin.role = 'admin_escola'
    school_admin.password = hash_password(school_admin.password)
    school_admin.school_id = school_id

    db.add(school_admin)
    db.commit()
    db.refresh(school_admin)

    return school_admin

@router.get('/admins')
def get_all_admins(current_user: User = Depends(get_current_user), 
                   db: Session = Depends(get_db)):
    if current_user.role != 'super_admin':
        raise HTTPException(403, detail='Operation not permitted!')
    
    admins = db.query(User).filter(User.role == 'admin_escola').all()

    if not admins:
        raise HTTPException(404, detail='Admins not Found!')
    
    return get_school_name(db, admins)