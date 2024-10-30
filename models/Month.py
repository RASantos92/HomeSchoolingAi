from pydantic import BaseModel
from typing import List
class Month(BaseModel):
    month_name: str
    topics: List[str]
    summary: str