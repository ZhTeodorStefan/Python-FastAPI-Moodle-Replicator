from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Any


class EvaluationTypes(Enum):

    EXAMEN_FINAL = 1
    ACTIVITATE_LAB = 2
    PROIECT = 3

class Evaluation(BaseModel):
    type: str
    weight: int

class Material(BaseModel):
    number: int
    file: str

class Course(BaseModel):
    code: str
    evaluation: List[Evaluation]
    course: Optional[List[Material]] = [
        {
          "number": 0,
          "file": "string"
        }
    ]
    lab: Optional[List[Material]] = [
        {
          "number": 0,
          "file": "string"
        }
    ]

    def serialize_course(self):
        return {
            "code": self.code,
            "evaluation": [{"type": e.type, "weight": e.weight} for e in self.evaluation],
            "course": [m.model_dump() if isinstance(m, Material) else m for m in self.course],
            "lab": [m.model_dump() if isinstance(m, Material) else m for m in self.lab],
        }


class CourseCreateRequest(BaseModel):
    code: str
    evaluation: List[Evaluation]

    def serialize_course(self):
        return {
            "code": self.code,
            "evaluation": [{"type": e.type, "weight": e.weight} for e in self.evaluation]
        }