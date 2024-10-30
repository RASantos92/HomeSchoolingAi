from djongo import models
from bson import ObjectId
from typing import List

class MCQ(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    
    # To Do:
    #  Need to initalize these feilds using the models from the dojogo import.
    question = str
    options = List[str]
    explanation = str
    answer = str
    grade_level : str
    subject_topic : str
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
