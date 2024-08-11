from pydantic import BaseModel
from typing import List
from models.MCQ import MCQ
class AssesmentTest(BaseModel):
    assesment_test_number: int
    subjects : List[MCQ]
