from pydantic import BaseModel
from typing import List

class WeeklyPlans(BaseModel):
    week_of_the_month: int
    week_topics : List[str]
    week_intro : str
    week_summary : str
    week_subjects : List[str]

class MonthBreakdown(BaseModel):
    month: str
    weeks : List[WeeklyPlans]