from peewee import MySQLDatabase, Model, CharField, IntegerField

db = MySQLDatabase(
    database='academia',
    user='root',
    password='root',
    host='localhost',
    port=3306
)

class BaseModel(Model):
    class Meta:
        database = db

class TestTable(BaseModel):
    name = CharField()
    age = IntegerField()

def create_and_test_table():
    try:
        if db.is_closed():
            db.connect()
        print("Connected to MariaDB.")

        db.create_tables([TestTable], safe=True)
        print("Table 'TestTable' created or already exists.")

        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ]
        with db.atomic():
            TestTable.insert_many(data).execute()
        print(f"Inserted {len(data)} records.")

        for record in TestTable.select():
            print(f"ID: {record.id}, Name: {record.name}, Age: {record.age}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if not db.is_closed():
            db.close()
        print("Connection closed.")

if __name__ == "__main__":
    create_and_test_table()
