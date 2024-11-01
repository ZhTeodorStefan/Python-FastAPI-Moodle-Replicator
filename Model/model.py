from peewee import Model, IntegerField, CharField, ForeignKeyField, CompositeKey, _StringField
from Model.database import db

class BaseModel(Model):
    class Meta:
        database = db

class Studenti(BaseModel):
    id_student = IntegerField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    grupa = CharField(unique=True)
    an_studiu = IntegerField()

    class Meta:
        db_table = "studenti"

class Profesori(BaseModel):
    id = IntegerField(primary_key=True)
    nume = _StringField()
    prenume = _StringField()
    email = _StringField(unique=True)
    grad_didactic = _StringField()
    tip_asociere = _StringField()
    afiliere = _StringField()

    class Meta:
        db_table = "profesori"

class Discipline(BaseModel):
    id_disciplina = IntegerField(primary_key=True)
    nume = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()

    class Meta:
        db_table = "discipline"
