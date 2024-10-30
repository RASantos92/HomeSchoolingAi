from pydantic import BaseModel
from typing import List
from models.Month import Month
class YearPlan(BaseModel):
    plan_number: int
    plan_subject: str
    months: List[Month]
