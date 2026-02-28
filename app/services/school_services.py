from models.models import School
from sqlalchemy.orm import Session

def get_school_name(db:Session, entidades):
    print('debug:', entidades)

    if type(entidades) != list:

        school = db.query(School).filter(School.id == entidades.school_id).first()
        print('Inside type not list:', school)

        if school is None:
            return entidades
        
        entidades.school_name = school.name
        print (entidades.school_name)

        return entidades

    for entidade in entidades:

        print(entidade.id)
        school = db.query(School).filter(School.id == entidade.school_id).first()
        if school is None:
            return entidades
        print(school)
        entidade.school_name = school.name
    
    return entidades
