from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {'name': 'Student 1', 'age': 20},
    {'name': 'Student 2', 'age': 18},
    {'name': 'Student 3', 'age': 16}
]

class Student(BaseModel):
    name: str
    age: int

@app.get('/students')
def user_list():
    return {'students': students}

@app.get('/students/{student_id}')
def user_detail(student_id: int):
    student_check(student_id)
    return {'student': students[student_id]}

@app.post('/students')
def user_add(student: Student):
    students.append(student)

    return {'student': students[-1]}

@app.put('/students/{student_id}')
def user_update(student: Student, student_id: int):
    student_check(student_id)
    students[student_id].update(student)

    return {'student': students[student_id]}

@app.delete('/students/{student_id}')
def user_delete(student_id: int):
    student_check(student_id)
    del students[student_id]

    return {'students': students}

def student_check(student_id):
    if not students[student_id]:
        raise HTTPException(status_code=404, detail='Student Not Found')
    
# STUDENTI

@app.get('/studenti')
def get_studenti():
    studenti = [student.__data__ for student in STUDENTI.select()]
    return {"studenti": studenti}

# PROFESORI

@app.get('/profesori')
def get_profesori():
    profesori = [profesor.__data__ for profesor in PROFESORI.select()]
    return {"profesori": profesori}

# DISCIPLINE

@app.get('/discipline')
def get_discipline():
    discipline = [disciplina.__data__ for disciplina in DISCIPLINE.select()]
    return {"discipline": discipline}