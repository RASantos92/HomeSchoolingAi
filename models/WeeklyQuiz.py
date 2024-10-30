from pydantic import BaseModel
from typing import List
from models.MCQ import MCQ
class WeeklyQuiz(BaseModel):
    subject_name : str
    subjects : List[MCQ]
