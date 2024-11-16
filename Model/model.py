from peewee import Model, IntegerField, CharField

class BaseModel(Model):
    class Meta:
        database = 'academia'

class STUDENTI(BaseModel):
    id_student = IntegerField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    grupa = CharField(unique=True)
    an_studiu = IntegerField()

    # class Meta:
    #     db_table = 'STUDENTI'

class PROFESORI(BaseModel):
    id = IntegerField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    grad_didactic = CharField()
    tip_asociere = CharField()
    afiliere = CharField()

    # class Meta:
    #     db_table = 'PROFESORI'

class DISCIPLINE(BaseModel):
    id_disciplina = IntegerField(primary_key=True)
    nume = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()

    # class Meta:
    #     db_table = 'DISCIPLINE'
