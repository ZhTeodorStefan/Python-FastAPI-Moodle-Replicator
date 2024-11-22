from fastapi import FastAPI, HTTPException
from Model.database import db
from Model.model import STUDENTI, PROFESORI, DISCIPLINE, StudentCreate, Profesor, Discipline, StudentUpdate

app = FastAPI()
db.create_tables([STUDENTI, PROFESORI, DISCIPLINE], safe = True)

# STUDENTI
student_exemplu:{
    "nume": "Popescu",
    "prenume": "Ion",
    "grupa": "A1",
    "an_studiu": 3
}

# CREATE
@app.post('/studenti')
def create_student(student: StudentCreate):
    student_nou = STUDENTI.create(
        nume=student.nume,
        prenume=student.prenume,
        grupa=student.grupa,
        an_studiu=student.an_studiu
    )
    return {"mesaj": "Student adaugat cu succes", "student": student_nou.__data__}

# READ
@app.get('/studenti/{student_id}')
def get_student(student_id: int):
    student = STUDENTI.get(STUDENTI.id_student == student_id)
    return {"student": student.__data__}
@app.get('/studenti')
def get_studenti():
    studenti = list(STUDENTI.select().dicts())
    return {"studenti": studenti}

# UPDATE
@app.put('/studenti/{student_id}')
def update_student(student_id: int, student_update: StudentUpdate):
    student = STUDENTI.get(STUDENTI.id_student == student_id)
    updated_data = student_update.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(student, key, value)
    student.save()
    return {"mesaj": "Student actualizat cu succes", "student": student.__data__}

# DELETE
@app.delete('/studenti/{student_id}')
def delete_student(student_id: int):
    try:
        student = STUDENTI.get(STUDENTI.id_student == student_id)
        student.delete_instance()
        return {"mesaj": "Student sters cu succes"}
    except STUDENTI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Studentul nu a fost gasit")

# PROFESORI
profesor_exemplu:{
    "nume": "Ionescu",
    "prenume": "Maria",
    "email": "maria.ionescu@example.com",
    "grad_didactic": "Profesor",
    "tip_asociere": "Titular",
    "afiliere": "Facultatea de Informatica"
}

# CREATE


# READ
@app.get('/profesori')
def get_profesori():
    profesori = list(PROFESORI.select().dicts())
    return {"profesori": profesori}
# UPDATE
# DELETE

# DISCIPLINE
disciplina_exemplu:{
    "nume": "Algoritmi Avansati",
    "an_studiu": 3,
    "nr_credite": 5
}

# CREATE
# READ
@app.get('/discipline')
def get_discipline():
    discipline = list(DISCIPLINE.select().dicts())
    return {"discipline": discipline}
# UPDATE
# DELETE