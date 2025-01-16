from peewee import CharField, AutoField, IntegerField
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
    nume: str = Field(..., min_length=2, max_length=30, description="Numele trebuie sa aiba intre 2 si 30 de caractere")
    prenume: str = Field(..., min_length=2, max_length=30, description="Prenumele trebuie sa aiba intre 2 si 30 de caractere")
    email: EmailStr = Field(..., description="Email-ul trebuie sa fie valid")
    grad_didactic: GradDidactic = Field(..., description="Gradul didactic trebuie sa fie 1 (asist), 2 (sef_lucr), 3 (conf), 4 (prof)")
    tip_asociere: TipAsociere = Field(..., description="Tipul de asociere trebuie sa fie 1 (titular), 2 (asociat), 3 (extern)")
    afiliere: str = Field(..., min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    # @field_validator('afiliere')
    # def check_alpha(cls, value):
    #     if value and not value.replace(" ", "").isalpha():
    #         raise ValueError('Afilierea trebuie sa contina doar litere')
    #     return value

    # @field_validator('grad_didactic')
    # def validate_grad_didactic(cls, value):
    #     try:
    #         print(GradDidactic(value))
    #         return GradDidactic(value)
    #     except ValueError:
    #         raise ValueError("Gradul didactic trebuie sa fie un numar intre 1 si 4.")
    #
    # @field_validator('tip_asociere')
    # def validate_tip_asociere(cls, value):
    #     try:
    #         print(TipAsociere(value))
    #         return TipAsociere(value)
    #     except ValueError:
    #         raise ValueError("Tipul de asociere trebuie sa fie un numar intre 1 si 3.")


class ProfesorUpdate(BaseModel):
    nume: Optional[str] = Field(None, min_length=2, max_length=30, description="Numele trebuie sa aiba intre 2 si 30 de caractere")
    prenume: Optional[str] = Field(None, min_length=2, max_length=30, description="Prenumele trebuie sa aiba intre 2 si 30 de caractere")
    email: Optional[EmailStr] = Field(None, description="Email-ul trebuie sa fie valid")
    grad_didactic: Optional[GradDidactic] = Field(None, description="Gradul didactic trebuie sa fie unul dintre: asist, sef_lucr, conf, prof")
    tip_asociere: Optional[TipAsociere] = Field(None, description="Tipul de asociere trebuie sa fie unul dintre: titular, asociat, extern")
    afiliere: Optional[str] = Field(None, min_length=2, max_length=100, description="Afilierea trebuie sa aiba intre 2 si 100 de caractere")

    # @field_validator('afiliere')
    # def check_alpha(cls, value):
    #     if value and not value.replace(" ", "").isalpha():
    #         raise ValueError('Afilierea trebuie sa contina doar litere')
    #     return value

    # @field_validator('grad_didactic')
    # def validate_grad_didactic(cls, value):
    #     try:
    #         return GradDidactic(value)
    #     except ValueError:
    #         raise ValueError("Gradul didactic trebuie sa fie un numar intre 1 si 4.")
    #
    # @field_validator('tip_asociere')
    # def validate_tip_asociere(cls, value):
    #     try:
    #         return TipAsociere(value)
    #     except ValueError:
    #         raise ValueError("Tipul de asociere trebuie sa fie un numar intre 1 si 3.")