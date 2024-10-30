from djongo import models
from bson import ObjectId
from typing import List
from models.Lesson import Lesson
class Day(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    
    day_name = str
    lessons = List[Lesson]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.day_name
