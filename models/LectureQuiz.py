from pydantic import BaseModel
from typing import List
from models.LectureMCQ import LectureMCQ
class LectureQuiz(BaseModel):
    questions : List[LectureMCQ]
