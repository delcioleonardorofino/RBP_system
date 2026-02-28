from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime

class User(Base):

    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False) #userRole.role
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=True)

class School(Base):

    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    adress = Column(String)

    def __str__(self):
        return self.name

class RevokedToken(Base):

    __tablename__='revoked_tokens'

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, nullable=False)
    revoked_at = Column(DateTime, default=datetime.utcnow())
    

class Turma(Base):
    
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number_of_students = Column(Integer, default=0)
    class_director_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    class_section = Column(String, nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)

class Student(Base):

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    turma_id = Column(Integer, ForeignKey('classes.id', ondelete='SET NULL'), nullable=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    age = Column(Integer, nullable=True)
    Fathers_name = Column(String, nullable=True)
    Mothers_name = Column(String, nullable=True)
    adress = Column(String, nullable=True)
    password = Column(String, nullable=False)
    student_number = Column(String, unique=True, index=True, nullable=True)

class Subject(Base):

    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)


class Grade(Base):

    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    Student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    value = Column(Integer, nullable=True)
    semestre = Column(Integer, nullable=False)
    published = Column(Boolean, default=False)

