from fastapi import FastAPI
from Model.database import db
from Model.model import STUDENTI, PROFESORI, DISCIPLINE

app = FastAPI()
db.create_tables([STUDENTI, PROFESORI, DISCIPLINE], safe = True)

# STUDENTI
@app.get('/studenti')
def get_studenti():
    studenti = [student.nume for student in STUDENTI.select()]
    return {"studenti": studenti}

# PROFESORI
@app.get('/profesori')
def get_profesori():
    profesori = [profesor.nume for profesor in PROFESORI.select()]
    return {"profesori": profesori}

# DISCIPLINE
@app.get('/discipline')
def get_discipline():
    discipline = [disciplina.nume for disciplina in DISCIPLINE.select()]
    return {"discipline": discipline}