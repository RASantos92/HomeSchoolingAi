from djongo import models
from bson import ObjectId
from typing import List
from models.MCQ import MCQ

class Lecture_Quiz(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    
    # To Do:
    #  Need to initalize these feilds using the models from the dojogo import.
    questions = List[MCQ]
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
