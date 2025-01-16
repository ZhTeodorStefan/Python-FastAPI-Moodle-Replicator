from fastapi import FastAPI, HTTPException, Query
from Model.disciplina_model import *
from Model.profesor_model import *
from Model.student_model import *

app = FastAPI()
db.create_tables([STUDENTI, PROFESORI, DISCIPLINE], safe = True)


# STUDENT
# CREATE
@app.post('/studenti', status_code = 201)
def create_student(student: StudentCreate):
    print(student.ciclu_studii)
    try:
        print(f"Date student primite: {student}")
        student_nou = STUDENTI.create(
            nume=student.nume,
            prenume=student.prenume,
            email=student.email,
            ciclu_studii = student.ciclu_studii,
            an_studiu=student.an_studiu,
            grupa=student.grupa
        )
        print(f"Student creat: {student_nou.__data__}")
        return {"mesaj": "Student adaugat cu succes", "student": student_nou.__data__}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Eroare: {ve}")
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

        if "nume" in updated_data:
            validate_nume_prenume(updated_data["nume"], "nume")
        if "prenume" in updated_data:
            validate_nume_prenume(updated_data["prenume"], "prenume")
        if "email" in updated_data and not validate_email(updated_data["email"]):
            raise HTTPException(status_code=422, detail="Email-ul furnizat nu este valid.")
        if "ciclu_studii" in updated_data and (updated_data["ciclu_studii"] < 1 or updated_data["ciclu_studii"] > 2):
            raise HTTPException(status_code=422, detail="Ciclul de studii trebuie sa fie 1(licenta) sau 2(master).")
        if "an_studiu" in updated_data and (updated_data["an_studiu"] < 1 or updated_data["an_studiu"] > 4):
            raise HTTPException(status_code=422, detail="Anul de studiu trebuie sa fie intre 1 si 4.")
        if "grupa" in updated_data and validate_grupa(updated_data["grupa"]):
            raise HTTPException(status_code=422, detail="Grupa trebuie sa fie de forma 1409A.")

        for key, value in updated_data.items():
            setattr(student, key, value)
        student.save()
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
@app.post('/profesori', status_code= 201)
def create_profesor(profesor: ProfesorCreate):
    print(profesor.grad_didactic)
    print(profesor.tip_asociere)
    try:
        print(f"Date profesor primite: {profesor}")
        profesor_nou = PROFESORI.create(
            nume=profesor.nume,
            prenume=profesor.prenume,
            email=profesor.email,
            grad_didactic=profesor.grad_didactic,
            tip_asociere=profesor.tip_asociere,
            afiliere=profesor.afiliere
        )
        print(f"Profesor creat: {profesor_nou.__data__}")
        return {"mesaj": "Profesor adaugat cu succes", "profesor": profesor_nou.__data__}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Eroare: {ve}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# READ
@app.get('/profesori/{profesor_id}')
def get_profesor(profesor_id: int):
    try:
        print(f"Interogare profesor cu id: {profesor_id}")
        profesor = PROFESORI.get(PROFESORI.id_profesor == profesor_id)
        print(f"Profesor găsit: {profesor.__data__}")
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
                    "self": f"/profesori/{profesor['id_profesor']}",
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
        profesor = PROFESORI.get(PROFESORI.id_profesor == profesor_id)
        updated_data = profesor_update.dict(exclude_unset=True)

        if "nume" in updated_data:
            validate_nume_prenume(updated_data["nume"], "nume")
        if "prenume" in updated_data:
            validate_nume_prenume(updated_data["prenume"], "prenume")
        if "email" in updated_data and not validate_email(updated_data["email"]):
            raise HTTPException(status_code=422, detail="Email-ul furnizat nu este valid.")
        if "grad_didactic" in updated_data and updated_data["grad_didactic"] not in GradDidactic:
            raise HTTPException(status_code=422, detail="Gradul didactic trebuie sa fie unul dintre: asist, sef_lucr, conf, prof.")
        if "tip_asociere" in updated_data and updated_data["tip_asociere"] not in TipAsociere:
            raise HTTPException(status_code=422, detail="Tipul de asociere trebuie sa fie unul dintre: titular, asociat, extern.")
        if "afiliere" in updated_data and (len(updated_data["afiliere"]) < 2 or len(updated_data["afiliere"]) > 100):
            raise HTTPException(status_code=422, detail="Afilierea trebuie sa aiba intre 2 si 100 de caractere.")

        for key, value in updated_data.items():
            setattr(profesor, key, value)
        profesor.save()
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DELETE
@app.delete('/profesori/{profesor_id}')
def delete_profesor(profesor_id: int):
    try:
        profesor = PROFESORI.get(PROFESORI.id_profesor == profesor_id)
        profesor.delete_instance()
        return {"mesaj": "Profesor șters cu succes"}
    except PROFESORI.DoesNotExist:
        raise HTTPException(status_code=404, detail="Profesorul nu a fost gasit")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")






# DISCIPLINA
# CREATE
@app.post('/discipline', status_code= 201)
def create_disciplina(disciplina: DisciplinaCreate):
    print(disciplina.TipDisciplina)
    print(disciplina.CategorieDisciplina)
    print(disciplina.TipExaminare)
    try:
        print(f"Date disciplina primite: {disciplina}")
        disciplina_noua = DISCIPLINE.create(
            cod=disciplina.cod,
            id_titular=disciplina.id_titular,
            nume_disciplina=disciplina.nume_disciplina,
            an_studiu=disciplina.an_studiu,
            nr_credite=disciplina.nr_credite,
            tip_disciplina=disciplina.tip_disciplina,
            categorie_disciplina=disciplina.categorie_disciplina,
            tip_examinare=disciplina.tip_examinare
        )
        print(f"Disciplina creata: {disciplina_noua.__data__}")
        return {"mesaj": "Disciplina adăugata cu succes", "disciplina": disciplina_noua.__data__}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Eroare: {ve}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# READ
@app.get('/discipline/{disciplina_id}')
def get_disciplina(disciplina_id: int):
    try:
        disciplina = DISCIPLINE.get(DISCIPLINE.cod == disciplina_id)
        return {
            "disciplina": {
                **disciplina.__data__,
                "links": {
                    "self": f"/discipline/{disciplina_id}",
                    "parent": "/discipline"
                }
            }
        }
    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost gasita")

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
                    "self": f"/discipline/{disciplina['cod']}",
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
        disciplina = DISCIPLINE.get(DISCIPLINE.cod == disciplina_id)
        updated_data = disciplina_update.dict(exclude_unset=True)

        if "cod" in updated_data and not (2 <= len(updated_data["cod"]) <= 10):
            raise HTTPException(status_code=422, detail="Codul trebuie sa aiba intre 2 si 10 caractere.")
        if "id_titular" in updated_data and PROFESORI.select().where(PROFESORI.id_profesor == updated_data["id_titular"]).exists():
            raise HTTPException(status_code=422, detail="ID-ul titularului nu este valid.")
        if "nume_disciplina" in updated_data:
            validate_nume_prenume(updated_data["nume_disciplina"], "nume disciplina")
        if "an_studiu" in updated_data and not (1 <= updated_data["an_studiu"] <= 4):
            raise HTTPException(status_code=422, detail="Anul de studiu trebuie sa fie intre 1 si 4.")
        if "nr_credite" in updated_data and not (1 <= updated_data["nr_credite"] <= 15):
            raise HTTPException(status_code=422, detail="Numarul de credite trebuie sa fie intre 1 si 15.")
        if "tip_disciplina" in updated_data and updated_data["tip_disciplina"] not in TipDisciplina:
            raise HTTPException(status_code=422, detail="Tipul disciplinei trebuie sa fie impusa, optionala sau liber aleasa.")
        if "categorie_disciplina" in updated_data and updated_data["categorie_disciplina"] not in CategorieDisciplina:
            raise HTTPException(status_code=422, detail="Categoria disciplinei trebuie sa fie domeniu, specialitate sau adiacenta.")
        if "tip_examinare" in updated_data and updated_data["tip_examinare"] not in TipExaminare:
            raise HTTPException(status_code=422, detail="Tipul examinarii trebuie sa fie examen sau colocviu.")

        for key, value in updated_data.items():
            setattr(disciplina, key, value)
        disciplina.save()
        return {
            "disciplina": {
                **disciplina.__data__,
                "links": {
                    "self": f"/discipline/{disciplina_id}",
                    "parent": "/discipline"
                }
            }
        }

    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost gasita")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")

# DELETE
@app.delete('/discipline/{disciplina_id}')
def delete_disciplina(disciplina_id: int):
    try:
        disciplina = DISCIPLINE.get(DISCIPLINE.cod == disciplina_id)
        disciplina.delete_instance()
        return {"mesaj": "Disciplina stearsa cu succes"}
    except DISCIPLINE.DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina nu a fost gasita")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Eroare: {e}")