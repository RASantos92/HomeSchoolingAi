from pydantic import BaseModel
from typing import List
class MCQ(BaseModel):
    questionNumber: int
    question: str
    options: List[str]
    explanation : str
    answer : str
    grade_level : str
    subject : str
    subject_topic : str