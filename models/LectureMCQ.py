from pydantic import BaseModel
from typing import List
class LectureMCQ(BaseModel):
    question: str
    options: List[str]
    explanation : str
    answer : str