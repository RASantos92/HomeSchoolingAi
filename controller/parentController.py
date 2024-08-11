from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List
from services.gptUtil import GptUtil
from models.AssesmentTest import AssesmentTest
load_dotenv()

class ParentController:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("myGptkey"))
        self.context = [{'role' : 'system' , 'content' : 'You are an expert educator. You are made for creating assessment test for students under 18 years of age. You also can create yearly, monthly and weekly lesson plans for every subject and every grade if needed.'}]
        self.assessmentNumber = ParentController.calculateAssessmentNumber()
        
    def assessmentTest(self, age : int, assumed_grade : int,subjects = ["Mathematics", "Language Arts", "Science", "Social Studies"]):
        temp_context = self.context.copy()
        for subject in subjects:
            intructions =  f"I need an assessment test for a {age} year old student. The **assumed_grade** is {assumed_grade} so please generate questions that range from one grade below and one grade above. The **Subject** is {subject}, and there should be 10 questions that address major topics in that subject for that assumed grade. Each multiple choice question (**MCQ**) sould follow this strict formating: - The **Subject** should be displayed- **Question number** for each question header. - Display the **Grade level** of the question. - **Question** sould be of a core topic in the subject. - **Options** should always be labeled with a number from 1)-4). - **Explanation** for the answer - **Answer** Should always start with the correct number option following the answer. Another important note is never repeat the same question. Always double check to make sure you have not generated the same question."
            self.context.append({'role' : 'user', 'content' : intructions})
            GptUtil.makeJsonAPICall(self, AssesmentTest,'./data/assessments', f'assessment{self.assessmentNumber}.json')
        self.context = temp_context
        print("Should have done it")



    @staticmethod
    def calculateAssessmentNumber():
        folder_path = './data/assessments'
        os.makedirs(folder_path, exist_ok = True)
        files = os.listdir(folder_path)
        return len(files)