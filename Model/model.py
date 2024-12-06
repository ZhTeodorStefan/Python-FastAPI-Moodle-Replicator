from typing import Optional

from peewee import Model, IntegerField, CharField, AutoField
from pydantic import BaseModel, Field, field_validator, EmailStr
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
    nume: str = Field(..., min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: str = Field(..., min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    grupa: str = Field(..., pattern=r'^\d{4}[A-B]$', description="Grupa trebuie sa fie formata din 4 cifre si o litera, ex: 1409A")
    an_studiu: int = Field(..., ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")

    @field_validator('nume', 'prenume')
    def check_alpha(cls, value):
        if not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

class StudentUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: Optional[str] = Field(None, min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    grupa: Optional[str] = Field(None, pattern=r'^\d{4}[A-B]$', description="Grupa trebuie sa fie formata din 4 cifre si o litera (A sau B), ex: 1409A")
    an_studiu: Optional[int] = Field(None, ge=1, le=4, description="Anul de studiu trebuie sa fie între 1 și 4")

    @field_validator('nume', 'prenume')
    def check_alpha(cls, value):
        if value and not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

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

class ProfesorCreate(BaseModel):
    nume: str = Field(..., min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: str = Field(..., min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    email: EmailStr = Field(..., description="Email-ul trebuie sa fie valid")
    grad_didactic: str = Field(..., min_length=2, max_length=30, description="Gradul didactic trebuie sa aiba intre 2 si 30 de caractere")
    tip_asociere: str = Field(..., min_length=2, max_length=30, description="Tipul de asociere trebuie sa aiba intre 2 si 30 de caractere")
    afiliere: str = Field(..., min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    @field_validator('nume', 'prenume', 'grad_didactic', 'tip_asociere', 'afiliere')
    def check_alpha(cls, value):
        if not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

class ProfesorUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=50, description="Numele trebuie sa aiba intre 2 si 50 de caractere")
    prenume: Optional[str] = Field(None, min_length=2, max_length=50, description="Prenumele trebuie sa aiba intre 2 si 50 de caractere")
    email: Optional[EmailStr] = Field(None, description="Email-ul trebuie sa fie valid")
    grad_didactic: Optional[str] = Field(None, min_length=2, max_length=30, description="Gradul didactic trebuie sa aiba intre 2 si 30 de caractere")
    tip_asociere: Optional[str] = Field(None, min_length=2, max_length=30, description="Tipul de asociere trebuie sa aiba intre 2 si 30 de caractere")
    afiliere: Optional[str] = Field(None, min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    @field_validator('nume', 'prenume', 'grad_didactic', 'tip_asociere', 'afiliere')
    def check_alpha(cls, value):
        if not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

class DISCIPLINE(ParentModel):
    id_disciplina = AutoField(primary_key=True)
    nume = CharField()
    an_studiu = IntegerField()
    nr_credite = IntegerField()

    class Meta:
        db_table = 'discipline'

class DisciplinaCreate(BaseModel):
    nume: str = Field(..., min_length=2, max_length=100, description="Numele disciplinei trebuie sa aiba intre 2 si 100 de caractere")
    an_studiu: int = Field(..., ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")
    nr_credite: int = Field(..., ge=1, le=15, description="Numarul de credite trebuie sa fie intre 1 si 15")

    @field_validator('nume')
    def check_alpha(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError('Numele disciplinei trebuie sa contina doar litere si spatii')
        return value

    @field_validator('an_studiu')
    def validate_an_studiu(cls, value):
        if not 1 <= value <= 4:
            raise ValueError('Anul de studiu trebuie sa fie intre 1 si 4')
        return value

    @field_validator('nr_credite')
    def validate_nr_credite(cls, value):
        if not 1 <= value <= 15:
            raise ValueError('Numarul de credite trebuie sa fie intre 1 si 15')
        return value

class DisciplinaUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=100, description="Numele disciplinei trebuie sa aiba intre 2 si 100 de caractere")
    an_studiu: Optional[int] = Field(None, ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")
    nr_credite: Optional[int] = Field(None, ge=1, le=15, description="Numarul de credite trebuie sa fie intre 1 si 15")

    @field_validator('nume')
    def check_alpha(cls, value):
        if value and not value.replace(" ", "").isalpha():
            raise ValueError('Numele disciplinei trebuie sa contina doar litere si spatii')
        return value

    @field_validator('an_studiu')
    def validate_an_studiu(cls, value):
        if not 1 <= value <= 4:
            raise ValueError('Anul de studiu trebuie sa fie intre 1 si 4')
        return value

    @field_validator('nr_credite')
    def validate_nr_credite(cls, value):
        if not 1 <= value <= 15:
            raise ValueError('Numarul de credite trebuie sa fie intre 1 si 15')
        return value