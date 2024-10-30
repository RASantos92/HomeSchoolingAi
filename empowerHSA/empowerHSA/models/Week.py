from djongo import models
from bson import ObjectId
from typing import List
from models.Day import Day
class Week(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    
    week_of_the_month = int 
    days = List[Day]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
