from pydantic import BaseModel, EmailStr, constr, ValidationError
from models.models import *
from utils import *


class AuthValidator(BaseModel):

    email: EmailStr

    password: constr(min_length=8, max_length=128)

    role: Roles

    def to_peewee(self) -> Auth:
        hashed_password = hash_password(self.password)
        return Auth(email=self.email, password=hashed_password, role=self.role.name)

def save_auth(email: str, password: str, role: Roles):
    try:
        validated_data = AuthValidator(email=email, password=password, role=role)

        auth = validated_data.to_peewee()
        auth.save()
        print("Inregistrare de autentificare salvata cu succes.")
    except ValidationError as e:
        print("Validare esuata:", e.json())
    except Exception as e:
        print("Eroare la salvare:", str(e))

def get_user_by_email(email: str) -> Auth:
    return Auth.select().where(Auth.email == email).first()