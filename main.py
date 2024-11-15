from fastapi import FastAPI
from Model.model import PROFESORI, STUDENTI, DISCIPLINE

app = FastAPI()

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