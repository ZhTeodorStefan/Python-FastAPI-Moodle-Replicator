from peewee import Model
from Model.database import db
from enum import Enum
from peewee_enum_field import EnumField
from typing import Optional

class ParentModel(Model):
    class Meta:
        database = db