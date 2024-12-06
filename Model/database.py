from peewee import MySQLDatabase

db = MySQLDatabase(
    database = 'academia',
    user = 'root',
    password = 'root',
    host = 'localhost',
    port = 3306)