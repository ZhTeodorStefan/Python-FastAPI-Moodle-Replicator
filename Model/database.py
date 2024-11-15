from peewee import MySQLDatabase
from Model.model import STUDENTI, PROFESORI, DISCIPLINE

print('creare variabila db')
db = MySQLDatabase(
    database = 'academia',
    user = 'root',
    password = 'root',
    host = 'localhost',
    port = 3306)
print('succes creare variabila db')

def create_tables():
    with db:
        print('Verificarea si crearea tabelelor...')
        # db.create_tables([STUDENTI, PROFESORI, DISCIPLINE])
        tables = [
            STUDENTI,
            PROFESORI,
            DISCIPLINE
        ]

        for table in tables:
            table_name = table._meta.table_name
            if not db.table_exists(table_name):
                print(f"Procesam modelul: {table} (nume: {table_name}) (tip: {type(table)})")
                db.create_tables([table])
                print(f'Tabelul "{table_name}" a fost creat.')
            else:
                print(f'Tabelul "{table_name}" exista deja.')