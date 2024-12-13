from peewee import IntegerField, CharField, ForeignKeyField
from pydantic import BaseModel, Field, field_validator
from Model.model import *
from Model.profesor_model import PROFESORI

class TipDisciplina(Enum):
    impusa = 1
    optionala = 2
    liber_aleasa = 3

class CategorieDisciplina(Enum):
    domeniu = 1
    specialitate = 2
    adiacenta = 3

class TipExaminare(Enum):
    examen = 1
    colocviu = 2

class DISCIPLINE(ParentModel):
    cod = CharField(primary_key=True)
    id_titular = ForeignKeyField(PROFESORI, backref='id_profesor')
    nume_disciplina = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()
    tip_disciplina = EnumField(TipDisciplina)
    categorie_disciplina = EnumField(CategorieDisciplina)
    tip_examinare = EnumField(TipExaminare)

    class Meta:
        db_table = 'discipline'

class DisciplinaCreate(BaseModel):
    cod: str = Field(..., min_length=2, max_length=10, description="Codul trebuie sa aiba intre 2 si 10 caractere")
    id_titular: int = Field(..., description="ID-ul titularului trebuie sa fie valid")
    nume_disciplina: str = Field(..., min_length=2, max_length=100, description="Numele disciplinei trebuie sa aiba intre 2 si 100 de caractere")
    an_studiu: int = Field(..., ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")
    nr_credite: int = Field(..., ge=1, le=15, description="Numarul de credite trebuie sa fie intre 1 si 15")
    tip_disciplina: TipDisciplina = Field(..., description="Tipul disciplinei trebuie sa fie impusa, optionala sau liber aleasa")
    categorie_disciplina: CategorieDisciplina = Field(..., description="Categoria disciplinei trebuie sa fie domeniu, specialitate sau adiacenta")
    tip_examinare: TipExaminare = Field(..., description="Tipul examinarii trebuie sa fie examen sau colocviu")

    @field_validator('nume_disciplina')
    def check_alpha(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError('Numele disciplinei trebuie sa contina doar litere si spatii')
        return value

class DisciplinaUpdate(BaseModel):
    cod: Optional[str] = Field(None, min_length=2, max_length=10, description="Codul trebuie sa aiba intre 2 si 10 caractere")
    id_titular: Optional[int] = Field(None, description="ID-ul titularului trebuie sa fie valid")
    nume_disciplina: Optional[str] = Field(None, min_length=2, max_length=100, description="Numele disciplinei trebuie sa aiba intre 2 si 100 de caractere")
    an_studiu: Optional[int] = Field(None, ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")
    nr_credite: Optional[int] = Field(None, ge=1, le=15, description="Numarul de credite trebuie sa fie intre 1 si 15")
    tip_disciplina: Optional[TipDisciplina] = Field(None, description="Tipul disciplinei trebuie sa fie impusa, optionala sau liber aleasa")
    categorie_disciplina: Optional[CategorieDisciplina] = Field(None, description="Categoria disciplinei trebuie sa fie domeniu, specialitate sau adiacenta")
    tip_examinare: Optional[TipExaminare] = Field(None, description="Tipul examinarii trebuie sa fie examen sau colocviu")

    @field_validator('nume_disciplina')
    def check_alpha(cls, value):
        if value and not value.replace(" ", "").isalpha():
            raise ValueError('Numele disciplinei trebuie sa contina doar litere si spatii')
        return value