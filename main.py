from fastapi import FastAPI, HTTPException, Query
from Model.model import *

app = FastAPI()
db.create_tables([STUDENTI, PROFESORI, DISCIPLINE], safe = True)

# STUDENT
# CREATE
@app.post('/studenti')
def create_student(student: StudentCreate):
    try:
        student_nou = STUDENTI.create(
            nume=student.nume,
            prenume=student.prenume,
            grupa=student.grupa,
            an_studiu=student.an_studiu
        )
        return {"mesaj": "Student adaugat cu succes", "student": student_nou.__data__}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# READ
@app.get('/studenti/{student_id}')
def get_student(student_id: int):
    try:
        student = STUDENTI.get(STUDENTI.id_student == student_id)
        return {
            "student": {
                **student.__data__,
                "links": {
                    "self": f"/studenti/{student_id}",
                    "parent": "/studenti"
                }
            }
        }
    except STUDENTI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Studentul nu a fost gasit")

@app.get('/studenti')
def get_studenti(
    page: int = Query(1, ge=1, description="Pagina trebuie sa fie cel putin 1"),
    limit: int = Query(10, ge=1, le=50, description="Limita trebuie sa fie intre 1 si 50")
):
    total_items = STUDENTI.select().count()
    total_pages = (total_items + limit - 1) // limit

    if page > total_pages > 0:
        raise HTTPException(status_code=416, detail="Range not satisfiable")

    offset = (page - 1) * limit
    studenti = list(STUDENTI.select().limit(limit).offset(offset).dicts())

    response = {
        "studenti": [
            {
                **student,
                "links": {
                    "self": f"/studenti/{student['id_student']}",
                    "parent": "/studenti"
                }
            }
            for student in studenti
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "links": {
            "self": f"/studenti?page={page}&limit={limit}",
            "first": f"/studenti?page=1&limit={limit}",
            "last": f"/studenti?page={total_pages}&limit={limit}" if total_pages > 0 else None,
            "next": f"/studenti?page={page + 1}&limit={limit}" if page < total_pages else None,
            "prev": f"/studenti?page={page - 1}&limit={limit}" if page > 1 else None
        }
    }
    return response

# UPDATE
@app.put('/studenti/{student_id}')
def update_student(student_id: int, student_update: StudentUpdate):
    try:
        student = STUDENTI.get(STUDENTI.id_student == student_id)
        updated_data = student_update.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(student, key, value)
        student.save()
        return {"mesaj": "Student actualizat cu succes", "student": student.__data__}
    except STUDENTI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Studentul nu a fost gasit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DELETE
@app.delete('/studenti/{student_id}')
def delete_student(student_id: int):
    try:
        student = STUDENTI.get(STUDENTI.id_student == student_id)
        student.delete_instance()
        return {"mesaj": "Student sters cu succes"}
    except STUDENTI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Studentul nu a fost gasit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# PROFESOR
# CREATE
@app.post('/profesori')
def create_profesor(profesor: ProfesorCreate):
    try:
        profesor_nou = PROFESORI.create(
            nume=profesor.nume,
            prenume=profesor.prenume,
            email=profesor.email,
            grad_didactic=profesor.grad_didactic,
            tip_asociere=profesor.tip_asociere,
            afiliere=profesor.afiliere
        )
        return {"mesaj": "Profesor adaugat cu succes", "profesor": profesor_nou.__data__}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# READ
@app.get('/profesori/{profesor_id}')
def get_profesor(profesor_id: int):
    try:
        profesor = PROFESORI.get(PROFESORI.id == profesor_id)
        return {
            "profesor": {
                **profesor.__data__,
                "links": {
                    "self": f"/profesori/{profesor_id}",
                    "parent": "/profesori"
                }
            }
        }
    except PROFESORI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Profesorul nu a fost gasit")

@app.get('/profesori')
def get_profesori(
    page: int = Query(1, ge=1, description="Pagina trebuie sa fie cel putin 1"),
    limit: int = Query(10, ge=1, le=50, description="Limita trebuie sa fie intre 1 si 50")
):
    total_items = PROFESORI.select().count()
    total_pages = (total_items + limit - 1) // limit

    if page > total_pages > 0:
        raise HTTPException(status_code=416, detail="Range not satisfiable")

    offset = (page - 1) * limit
    profesori = list(PROFESORI.select().limit(limit).offset(offset).dicts())

    response = {
        "profesori": [
            {
                **profesor,
                "links": {
                    "self": f"/profesori/{profesor['id']}",
                    "parent": "/profesori"
                }
            }
            for profesor in profesori
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "links": {
            "self": f"/profesori?page={page}&limit={limit}",
            "first": f"/profesori?page=1&limit={limit}",
            "last": f"/profesori?page={total_pages}&limit={limit}" if total_pages > 0 else None,
            "next": f"/profesori?page={page + 1}&limit={limit}" if page < total_pages else None,
            "prev": f"/profesori?page={page - 1}&limit={limit}" if page > 1 else None
        }
    }
    return response

# UPDATE
@app.put('/profesori/{profesor_id}')
def update_profesor(profesor_id: int, profesor_update: ProfesorUpdate):
    try:
        profesor = PROFESORI.get(PROFESORI.id == profesor_id)
        updated_data = profesor_update.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(profesor, key, value)
        profesor.save()
        return {"mesaj": "Profesor actualizat cu succes", "profesor": profesor.__data__}
    except PROFESORI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Profesorul nu a fost gasit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DELETE
@app.delete('/profesori/{profesor_id}')
def delete_profesor(profesor_id: int):
    try:
        profesor = PROFESORI.get(PROFESORI.id == profesor_id)
        profesor.delete_instance()
        return {"mesaj": "Profesor șters cu succes"}
    except PROFESORI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Profesorul nu a fost gasit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DISCIPLINA
# CREATE
@app.post('/discipline')
def create_disciplina(disciplina: DisciplinaCreate):
    try:
        disciplina_noua = DISCIPLINE.create(
            nume=disciplina.nume,
            an_studiu=disciplina.an_studiu,
            nr_credite=disciplina.nr_credite
        )
        return {"mesaj": "Disciplina adăugata cu succes", "disciplina": disciplina_noua.__data__}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# READ
@app.get('/discipline/{disciplina_id}')
def get_disciplina(disciplina_id: int):
    try:
        disciplina = DISCIPLINE.get(DISCIPLINE.id_disciplina == disciplina_id)
        return {
            "disciplina": {
                **disciplina.__data__,
                "links": {
                    "self": f"/discipline/{disciplina_id}",
                    "parent": "/discipline"
                }
            }
        }
        return {"disciplina": disciplina.__data__}
    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost găsita")

@app.get('/discipline')
def get_discipline(
    page: int = Query(1, ge=1, description="Pagina trebuie sa fie cel putin 1"),
    limit: int = Query(10, ge=1, le=50, description="Limita trebuie sa fie intre 1 si 50")
):
    total_items = DISCIPLINE.select().count()
    total_pages = (total_items + limit - 1) // limit

    if page > total_pages > 0:
        raise HTTPException(status_code=416, detail="Range not satisfiable")

    offset = (page - 1) * limit
    discipline = list(DISCIPLINE.select().limit(limit).offset(offset).dicts())

    response = {
        "discipline": [
            {
                **disciplina,
                "links": {
                    "self": f"/discipline/{disciplina['id_disciplina']}",
                    "parent": "/discipline"
                }
            }
            for disciplina in discipline
        ],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages
        },
        "links": {
            "self": f"/discipline?page={page}&limit={limit}",
            "first": f"/discipline?page=1&limit={limit}",
            "last": f"/discipline?page={total_pages}&limit={limit}" if total_pages > 0 else None,
            "next": f"/discipline?page={page + 1}&limit={limit}" if page < total_pages else None,
            "prev": f"/discipline?page={page - 1}&limit={limit}" if page > 1 else None
        }
    }
    return response

# UPDATE
@app.put('/discipline/{disciplina_id}')
def update_disciplina(disciplina_id: int, disciplina_update: DisciplinaUpdate):
    try:
        disciplina = DISCIPLINE.get(DISCIPLINE.id_disciplina == disciplina_id)
        updated_data = disciplina_update.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(disciplina, key, value)
        disciplina.save()
        return {"mesaj": "Disciplina actualizata cu succes", "disciplina": disciplina.__data__}
    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost găsita")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DELETE
@app.delete('/discipline/{disciplina_id}')
def delete_disciplina(disciplina_id: int):
    try:
        disciplina = DISCIPLINE.get(DISCIPLINE.id_disciplina == disciplina_id)
        disciplina.delete_instance()
        return {"mesaj": "Disciplina stearsa cu succes"}
    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost găsita")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")