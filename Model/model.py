from peewee import Model
from Model.database import db
from enum import Enum
from peewee_enum_field import EnumField
from typing import Optional
import re

class ParentModel(Model):
    class Meta:
        database = db

def validate_email(email: str) -> bool:
    """
    Validează dacă un email are un format corect.
    :param email: Adresa de email de validat
    :return: True dacă email-ul este valid, altfel False
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None