from peewee import Model, IntegerField, CharField
from Model.database import db

class BaseModel(Model):
    class Meta:
        database = db

class STUDENTI(BaseModel):
    id_student = IntegerField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    grupa = CharField(unique=True)
    an_studiu = IntegerField()

    class Meta:
        db_table = 'studenti'

class PROFESORI(BaseModel):
    id = IntegerField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    grad_didactic = CharField()
    tip_asociere = CharField()
    afiliere = CharField()

    class Meta:
        db_table = 'profesori'

class DISCIPLINE(BaseModel):
    id_disciplina = IntegerField(primary_key=True)
    nume = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()

    class Meta:
        db_table = 'discipline'
