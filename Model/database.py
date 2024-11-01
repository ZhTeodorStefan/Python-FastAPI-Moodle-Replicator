from peewee import MySQLDatabase
from model import PROFESORI, STUDENTI, DISCIPLINE

db = MySQLDatabase(database = 'Date profesori/studenti/discipline', user = 'idk', password = 'idk', host = 'idk', port = 'idk')

def create_tables():
    with db:
        db.create_tables([PROFESORI, STUDENTI, DISCIPLINE])