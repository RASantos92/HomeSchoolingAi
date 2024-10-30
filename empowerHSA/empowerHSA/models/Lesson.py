from djongo import models
from bson import ObjectId
from typing import List
from models.MCQ import MCQ
from models.Lecture_Quiz import Lecture_Quiz
class Lesson(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # To Do:
    #  Need to set up these feilds with the models import from djongo 
    lesson_summary = str
    lesson_subject = str
    lesson_topics = List[str]
    lesson_daily_intro = str
    lesson_sub_topics = List[str]
    lesson_questions = List[MCQ] ## This will be a list of MCQs
    lesson_questions_grade = float
    lesson_quiz = Lecture_Quiz ## This will be a instance of a Quiz
    lesson_quiz_grade = float ## This will be a float
    lesson_complete = bool ## This will be a bool
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
