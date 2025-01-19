from repository import save_auth
from models.models import *

with database:
    database.drop_tables([Auth])
    database.create_tables([Auth])

    save_auth("admin@gmail.com", "Pass.1234", Roles.ADMIN)
    save_auth("student@gmail.com", "Pass.1234", Roles.STUDENT)
    save_auth("profesor@gmail.com", "Pass.1234", Roles.PROFESSOR)