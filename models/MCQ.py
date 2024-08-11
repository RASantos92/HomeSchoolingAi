from pydantic import BaseModel
from typing import List
class MCQ(BaseModel):
    questionNumber: int
    scenario: str
    question: str
    options: List[str]
    explanation : str
    answer : str
    grade_level : str
    subject : str