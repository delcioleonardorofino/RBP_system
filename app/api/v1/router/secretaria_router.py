from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.schemas import UserOut, CreateStudent
from models.models import User, Student, Turma
from dependencies.security import get_current_user, hash_password

router = APIRouter(prefix='/secretaria', tags=['secretaria'])


@router.get('/students', response_model=list[UserOut])
def get_all_users_of_school(
                            current_user: User = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    if current_user.role != 'secretaria':
        raise HTTPException(403, detail='Operation not permitted!')
    
    students = db.query(Student).filter(Student.school_id == current_user.school_id).all()

    return students


@router.post('/sign_student')
def create_student(
                    student_data: CreateStudent,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    
    if current_user.role != 'secretaria':
        raise HTTPException(403, detail='Operation not permitted!')

    turma = db.query(Turma).filter(Turma.name == student_data.turma_name, Turma.school_id == current_user.school_id).first()

    if not turma:
        raise HTTPException(404, detail='Class not found!')

    if student_data.turma_name:
        student_data_dict = student_data.model_dump()
        student_data_dict.pop('turma_name', None)  # Remove the turma_name from the student_data to avoid issues when creating the Student object
        student_data = CreateStudent(**student_data_dict)


    new_student = Student(**student_data.model_dump())
    new_student.school_id = current_user.school_id
    new_student.turma_id = turma.id
    new_student.password = hash_password(str(new_student.full_name) + str(new_student.id))  # Default password, should be changed by the student later
    print(new_student)
    
    turma.number_of_students += 1
   
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

