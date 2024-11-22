from peewee import Model, IntegerField, CharField, AutoField
from pydantic import BaseModel
from Model.database import db

class ParentModel(Model):
    class Meta:
        database = db

class STUDENTI(ParentModel):
    id_student = AutoField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    grupa = CharField()
    an_studiu = IntegerField()

    class Meta:
        db_table = 'studenti'

class StudentCreate(BaseModel):
    nume: str
    prenume: str
    grupa: str
    an_studiu: int

class StudentUpdate(BaseModel):
    nume: str = None
    prenume: str = None
    grupa: str = None
    an_studiu: int = None

class PROFESORI(ParentModel):
    id = AutoField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    grad_didactic = CharField()
    tip_asociere = CharField()
    afiliere = CharField()

    class Meta:
        db_table = 'profesori'

class Profesor(BaseModel):
    nume: str
    prenume: str
    email: str
    grad_didactic: str
    tip_asociere: str
    afiliere: str

class DISCIPLINE(ParentModel):
    id_disciplina = AutoField(primary_key=True)
    nume = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()

    class Meta:
        db_table = 'discipline'

class Discipline(BaseModel):
    nume: str
    an_studiu: int
    nr_credite: int