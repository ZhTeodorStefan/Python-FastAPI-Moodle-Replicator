from peewee import MySQLDatabase

db = MySQLDatabase(database = 'academia', user = 'root', password = 'root', host = 'localhost', port = 3306)

def create_tables():
    with db:
        print('Creating tables...')
        db.create_tables(["studenti", "profesori", "discipline"])
