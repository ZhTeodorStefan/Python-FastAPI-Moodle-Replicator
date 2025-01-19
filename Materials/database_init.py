from database_config import course_data_collection
from models import EvaluationTypes

course_data = [
    {
        "code": "PC1",
        "evaluation": [
            {"type": EvaluationTypes.EXAMEN_FINAL.name, "weight": 50},
            {"type": EvaluationTypes.ACTIVITATE_LAB.name, "weight": 50},
        ],
        "course": [
            {"number": 1, "file": "conspectPC1-partea1.pdf"},
            {"number": 2, "file": "conspectPC1-partea2.pdf"},
            {"number": 3, "file": "conspectPC1-partea3.pdf"},
        ],
        "lab": [
            {"number": 1, "file": "laboratorPC.txt"},
        ]
    },

    {
        "code": "MN101",
        "evaluation": [
            {"type": EvaluationTypes.EXAMEN_FINAL.name, "weight": 60},
            {"type": EvaluationTypes.ACTIVITATE_LAB.name, "weight": 10},
            {"type": EvaluationTypes.PROIECT.name, "weight": 30},
        ],
        "course": [
            {"number": 1, "file": "CURS1.pdf"},
            {"number": 2, "file": "CURS2.pdf"},
            {"number": 3, "file": "CURS3.pdf"},
        ],
        "lab": [
            {"number": 1, "file": "LAB1.txt"},
        ]
    },
]

course_data_collection.create_index("code", unique=True)

course_data_collection.delete_many({})

course_data_collection.insert_many(course_data)