from pydantic import BaseModel
from typing import List

class Subject(BaseModel):
    subject_name : str
    subject_topic : str
    subject_daily_intro : str
    subject_daily_sub_topics : List[str]
    subject_topic_daily_summary : str
    
class Day(BaseModel):
    day_name : str
    subjects : list[Subject]

class Week(BaseModel):
    days: List[Day]
    