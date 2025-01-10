from peewee import CharField, AutoField
from pydantic import BaseModel, Field, field_validator, EmailStr
from Model.model import *

class GradDidactic(Enum):
    asist = 1
    sef_lucr = 2
    conf = 3
    prof = 4

class TipAsociere(Enum):
    titular = 1
    asociat = 2
    extern = 3

class PROFESORI(ParentModel):
    id_profesor = AutoField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    grad_didactic = EnumField(GradDidactic)
    tip_asociere = EnumField(TipAsociere)
    afiliere = CharField()

    class Meta:
        db_table = 'profesori'

class ProfesorCreate(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: str = Field(..., min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    email: EmailStr = Field(..., description="Email-ul trebuie sa fie valid")
    grad_didactic: GradDidactic = Field(..., description="Gradul didactic trebuie sa fie unul dintre: asist, sef_lucr, conf, prof")
    tip_asociere: TipAsociere = Field(..., description="Tipul de asociere trebuie sa fie unul dintre: titular, asociat, extern")
    afiliere: str = Field(..., min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    @field_validator('nume', 'prenume', 'afiliere')
    def check_alpha(cls, value):
        if value is not None and not value.isalpha():
            raise ValueError('Numele, prenumele si afilierea trebuie sa contina doar litere')
        return value

class ProfesorUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: Optional[str] = Field(None, min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    email: Optional[EmailStr] = Field(None, description="Email-ul trebuie sa fie valid")
    grad_didactic: Optional[GradDidactic] = Field(None, description="Gradul didactic trebuie sa fie unul dintre: asist, sef_lucr, conf, prof")
    tip_asociere: Optional[TipAsociere] = Field(None, description="Tipul de asociere trebuie sa fie unul dintre: titular, asociat, extern")
    afiliere: Optional[str] = Field(None, min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    @field_validator('nume', 'prenume', 'afiliere')
    def check_alpha(cls, value):
        if value is not None and not value.isalpha():
            raise ValueError('Numele, prenumele si afilierea trebuie sa contina doar litere')
        return value