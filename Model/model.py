from fastapi import HTTPException

from peewee import Model
from Model.database import db
from enum import Enum
from peewee_enum_field import EnumField
from typing import Optional
import re

class ParentModel(Model):
    class Meta:
        database = db

def validate_nume_prenume(value: str, field_name: str) -> None:
    if not (2 <= len(value) <= 30):
        raise HTTPException(status_code=422, detail=f"{field_name.capitalize()} trebuie sa aiba intre 2 si 30 de caractere.")
    if not value.isalpha():
        raise HTTPException(status_code=422, detail=f"{field_name.capitalize()} trebuie sa contina doar litere.")

def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None