from peewee import IntegerField, CharField, AutoField
from pydantic import BaseModel, Field, field_validator, EmailStr
from Model.model import *

class CicluStudii(Enum):
    licenta = 1
    master = 2

class STUDENTI(ParentModel):
    id_student = AutoField(primary_key=True)
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    ciclu_studii = EnumField(CicluStudii)
    an_studiu = IntegerField()
    grupa = CharField()

    class Meta:
        db_table = 'studenti'

class StudentCreate(BaseModel):
    nume: str = Field(..., min_length=2, max_length=30, description="Numele trebuie sa aiba intre 2 si 30 de caractere")
    prenume: str = Field(..., min_length=2, max_length=30, description="Prenumele trebuie sa aiba intre 2 si 30 de caractere")
    email: EmailStr = Field(..., description="Email-ul trebuie sa fie valid")
    ciclu_studii: CicluStudii = Field(..., description="Ciclul de studii trebuie sa fie licenta sau master")
    an_studiu: int = Field(..., ge=1, le=4, description="Anul de studiu trebuie sa fie intre 1 si 4")
    grupa: str = Field(..., pattern=r'^\d{4}[A-B]$', description="Grupa trebuie sa fie formata din 4 cifre si o litera, ex: 1409A")

    @field_validator('nume', 'prenume')
    def check_alpha(cls, value):
        if not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

class StudentUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=30, description="Numele trebuie sa aiba intre 2 si 30 de caractere")
    prenume: Optional[str] = Field(None, min_length=2, max_length=30, description="Prenumele trebuie sa aiba intre 2 si 30 de caractere")
    email: Optional[EmailStr] = Field(None, description="Email-ul trebuie sa fie valid")
    ciclu_studii: Optional[CicluStudii] = Field(None, description="Ciclul de studii trebuie sa fie licenta sau master")
    an_studiu: Optional[int] = Field(None, ge=1, le=4, description="Anul de studiu trebuie sa fie între 1 și 4")
    grupa: Optional[str] = Field(None, pattern=r'^\d{4}[A-B]$', description="Grupa trebuie sa fie formata din 4 cifre si o litera (A sau B), ex: 1409A")

    @field_validator('nume', 'prenume')
    def check_alpha(cls, value):
        if value and not value.isalpha():
            raise ValueError('Numele si prenumele trebuie sa contina doar litere')
        return value

def validate_grupa(grupa: str) -> bool:
    """
    Validează dacă o grupă respectă formatul cerut.
    :param grupa: String-ul reprezentând grupa de validat.
    :return: True dacă grupa este validă, altfel False.
    """
    grupa_regex = r'^[1-4]\d{3}[AB]$'
    return re.match(grupa_regex, grupa) is not None