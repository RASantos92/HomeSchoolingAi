from pydantic import BaseModel
from typing import List

class Lesson(BaseModel):
    title : str
    lecture : str
    summary : str
    subject : str
    main_topic : str
    sub_topics :List[str]
    wikipedia_refrences : List[str]

class Day(BaseModel):
    lessons : List[Lesson]