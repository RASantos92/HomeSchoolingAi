from openai import OpenAI
from dotenv import load_dotenv
import os
from services.gptUtil import GptUtil
from models.LectureMCQ import LectureMCQ
from models.AssesmentTest import AssesmentTest
from services.jsonDataCleaning import JsonDataCleaning
from models.YearPlan import YearPlan
from models.WeeklyPlans import MonthBreakdown
from pathlib import Path
from models.WeeklyBreakdown import Week
from models.Lesson import Day
from services.jsonUtil import JsonUtil
import json
from typing import List
from models.LectureQuiz import LectureQuiz
import random
from datetime import datetime
from models.WeeklyQuiz import WeeklyQuiz
import copy
load_dotenv()
month_key = {
            "08" : 0,
            "09" : 1, 
            "10" : 2, 
            "11" : 3, 
            "12" : 4,
            "01" : 5,
            "02" : 6,
            "03" : 7,
            "04" : 8,
            "05" : 9
        }
week_key = {
    8 : 0,
    15 : 1,
    22 : 2,
    32 : 3
}
class Parent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("myGptkey"))
        self.context = [{'role' : 'system' , 'content' : 'You are an expert educator. You are made for creating assessment test for a single student under 18 years of age. You also can create yearly, monthly and weekly lesson plans for every subject and every grade if needed. Take into accout that it is only one student from home. So no group work at all. The student will rely on asking you questions and refering to refrences that you may provide for Wikipedia. Do not create lesson plans that rely on the student having supplies or item.'}]
        self.assessmentNumber = Parent.calculateAssessmentNumber() + 1
        
    def assessmentTest(self, age : int, assumed_grade : int, subjects = ["Mathematics", "Language Arts", "Science", "Social Studies"]):
        temp_context = copy.deepcopy(self.context)
        for subject in subjects:
            intructions =  f"I need an assessment test for a {age} year old student. The **assumed_grade** is {assumed_grade} so please generate questions that range from one grade below and one grade above. The **Subject** is {subject}, and there should be 10 questions that address major topics in that subject for that assumed grade. Each multiple choice question (**MCQ**) should follow this strict formating: - The **Subject** should be displayed- **Question number** for each question header. - Display the **Grade level** of the question. - **Question** should be of a core topic in the subject. - **Options** should always be labeled with a number from 1)-4). - **Explanation** for the answer - **Answer** Should always start with the correct number option following the answer - **Subject Topic** the particular topic that this question covers. Another important note is never repeat the same question. Always double check to make sure you have not generated the same question."
            self.context.append({'role' : 'user', 'content' : intructions})
            GptUtil.makeJsonAPICall(self, AssesmentTest,'./data/assessments', f'assessment{self.assessmentNumber}.json')
        self.context = copy.deepcopy(temp_context)
        JsonDataCleaning.restructureAssessmentData(f'./data/assessments/assessment{self.assessmentNumber}.json')
        

    def generateLectureQuestionsAndQuiz(self, file_path, lesson_data):
        lecture = lesson_data['lecture']
        temp_context = copy.deepcopy(self.context)
        split_lecture = lecture.split("[p]")
        
        lecture_MCQ = []
        temp_chapter = ""
        for index, chapter in enumerate(split_lecture):
            temp_chapter += f"{chapter}"
            if len(temp_chapter.split(" ")) < 75: 
                continue
            if index == len(split_lecture)-1 and not temp_chapter:
                break
            lecture_MCQ.append(self.generateChapterQuestion(chapter))
            temp_chapter = ""
        
        lecture_questions = [q.question for q in lecture_MCQ]
        instructions = f"{lecture}:\n That is the lecture for the day. I need you to generate a 10 questions quiz with all multiple choice question. Each multiple choice question should follow this strict formating: - The **Question** should be of a what was covered in the lecture. - **Options** should always be labeled with a number from 1)-4). - **Explanation** for the answer - **Answer** Should always start with the correct number option following the answer. Another important note is never repeat the same question. Always double check to make sure you have not generated the same question. Also here is a list of questions to avoid: \n {'\n'.join(lecture_questions)}"
        self.context.append({'role' : 'user', 'content' : instructions})
        compleation = GptUtil.makeJsonAPICall(self, LectureQuiz)
        quiz = compleation.choices[0].message.parsed
        quiz_questions =  [ {
                'question': q.question,
                'options' : random.sample(q.options, len(q.options)), 
                'explanation' : q.explanation,
                'answer' : q.answer
            }
            for q in quiz.questions]
        lecture_questions =  [ {
                'question': q.question,
                'options' : random.sample(q.options, len(q.options)), 
                'explanation' : q.explanation,
                'answer' : q.answer
            }
            for q in lecture_MCQ]
        self.context = copy.deepcopy(temp_context)
        lesson_data['quiz'] = quiz_questions
        lesson_data['lecture_questions'] = lecture_questions
        final_json_data = [{'lessons':[lesson_data]}]
        final_json_data[0]
        with open(file_path, 'w') as json_file:
            json.dump(final_json_data, json_file, indent=4)
        return lesson_data

    def generateChapterQuestion(self,lecture_chapter:str)-> List:
        temp_context = copy.deepcopy(self.context)
        instructions = f"{lecture_chapter}\n this is a chapter of the lecture. I need a single multiple choice question (**MCQ**) about the lecture material. the multiple choice question (**MCQ**) should follow this strict formating: - The **Question** sould be of a core topic in the givin material. - **Options** should always be labeled with a number from 1)-4). - **Explanation** for the answer - **Answer** Should always start with the correct number option following the answer"
        self.context.append({'role' : 'user', 'content' : instructions})
        compleation = GptUtil.makeJsonAPICall(self,LectureMCQ)
        self.context = copy.deepcopy(temp_context)
        return compleation.choices[0].message.parsed
        
        
    def createYearlyLessonPlanForSubject(self,name:str, age: int, grade_level: int, subject: str):
        temp_context = copy.deepcopy(self.context)
        instructions = f"I need a yearly lesson plan for my home school student. This lesson plan should break down the specific topics in this subject **{subject}** that a public school student would learn at {grade_level} grade level through out the year. For the a {age} year old. I need it broken down in this strict format: - **month_name** the month of the school year starting in August There should be 10 months in total with each month having the following: - **Topics** each month should have specific topics that the students need to learn. Each topic make bold. - **Summary** each month should have a summary of What the student will learn and how it will help them moving forward int the school year."
        if Path(f'./data/yearPlan/{name}/{grade_level}{age}{subject}yearPlan{Parent.calculateYearPlanNumber(name)}').exists():
            print(f"You already have created a year plan for {name} with the subject {subject} at the {grade_level}th grade level")
            return None
        self.context.append({'role' : 'user', 'content': instructions})
        GptUtil.makeJsonAPICall(self, YearPlan, f'./data/yearPlan/{name}', f'{grade_level}{age}{subject}yearPlan{Parent.calculateYearPlanNumber(name)}.json')
        self.context = copy.deepcopy(temp_context)
        
    def createLessonPlanForSubject(self,name:str, age: int, grade_level: int, subject: str, duration: str):
        current_month = datetime.now().strftime('%m')
        temp_context = copy.deepcopy(self.context)
        instructions = f"I need a lesson plan for a home school student. This lesson plan should break down the specific topics in this subject **{subject}** that a public school student would learn at {grade_level} grade level through out the year. For the a {age} year old. I need it broken down in this strict format: - **month_name** the month of the school year starting in {current_month} There should be {duration} months in total with each month having the following: - **Topics** each month should have specific topics that the students need to learn. Each topic make bold. - **Summary** each month should have a summary of What the student will learn and how it will help them moving forward in the school year."
        if Path(f'./data/yearPlan/{name}/{grade_level}{age}{subject}yearPlan{Parent.calculateYearPlanNumber(name)}').exists():
            print(f"You already have created a year plan for {name} with the subject {subject} at the {grade_level}th grade level")
            return None
        self.context.append({'role' : 'user', 'content': instructions})
        GptUtil.makeJsonAPICall(self, YearPlan, f'./data/yearPlan/{name}', f'{grade_level}{age}{subject}yearPlan{Parent.calculateYearPlanNumber(name)}.json')
        self.context = copy.deepcopy(temp_context) 

    def createWeeklyLessonPlanForStudent(self, name:str):
        usableData = JsonDataCleaning.retriveStudentsFullYearPlanAsDictionary(name)
        temp_context = copy.deepcopy(self.context)
        if Path(f'./data/yearPlan/{name}/weeklyPlans').exists():
            print(f'You have already generated weekly plans for {name}')
            return None
        if not usableData:
            print("That name has not created a year plan yet")
            return None
        for month, subjects in usableData.items():
            print("*"*1000)
            print(month, subjects)
            monthly_summary = ""
            for subject, info in subjects.items():
                monthly_summary += f"Subject = {subject}, Topics for subject = {' '.join(info['topics'])} Monthly summary for subject = {info['monthly_subject_summary']}\n"
            instructions = f"I need you to create a weekly breakdown for the month of {month}. Here is the monthly summary of what the student will be learning: {monthly_summary}. \n With this information I need you to break down the weeks of {month} to cover all these topics for each subject. Each week should have a topic from each subject. Assume that each month has only 4 weeks never go above 4 weeks. The infromation should be broken down in this strict format: - **Week_of_the_month** will be represented as an integer - **week_topics** should list the topics that will be covered this week should list at least one topic from each subject. - **week_intro** should be a summary of what to expect to learn in all topics this week. - **week_summary** this should be a summary for the end of the week to summarize what was learned."
            self.context.append({'role':'user', 'content': instructions})
            GptUtil.makeJsonAPICall(self, MonthBreakdown, f'./data/yearPlan/{name}/weeklyPlans', "weeklyPlans.json")
            self.context = copy.deepcopy(temp_context)

    def createWeeklyBreakdown(self, name:str, month:str, week:str):
        temp_context = copy.deepcopy(self.context)
        if month not in month_key:
            print("this is summer break")
            return None
        data = JsonUtil.getStudentsWeeklyPlan(name)
        if data == None:
            return None
        week = int(week)-1
        # print(data[month_key[month]]["weeks"][week])
        instructions = f"I need you to break down this weeks learning plans for Monday through Friday, A full week should always be generated, according to the following information : \n Subjects = {' '.join(data[month_key[month]]["weeks"][week]['week_subjects']).replace('+', ' advanced')} subjects are in order of when they will be taken. Here are the topics for each subject that the student will learn {' '.join(data[month_key[month]]["weeks"][week]['week_topics'])} Their order corresponds with the order of the subjects. Here is the summary of the week : {data[month_key[month]]["weeks"][week]['week_summary']}. Each subject and their respective topics should have the following: - **Subject_daily_intro** this is where you talk about what the student will learn and what was learned yesterday if it is not on a Monday. If the day is Monday DO NOT REFRENCE WHAT WAS TALKED ABOUT LAST CLASS. - **subject_daily_sub_topics** these are optional sub topics that might be learned along side the main topic. **Subject_topic_daily_summary** This is an over all summary about the what should be learned on the subject with repective topic. Each day should have all subjects"
        self.context.append({'role':'user', 'content': instructions})
        if Path(f'./data/yearPlan/{name}/weeklyBreakdown/{month}/{week}').exists():
            print("You have already generated a weekly breakdown for this week.")
            return None
        GptUtil.makeJsonAPICall(self,Week,f'./data/yearPlan/{name}/weeklyBreakdown/{month}/{week}',"breakdown.json")
        self.context = copy.deepcopy(temp_context)
        
    def createDailyBreakDown(self,name:str, month:str, week:str, day:str ):
        month, week, day = month, int(week), day
        folder_path = Path(f'./data/yearPlan/{name}/weeklyBreakdown/{month}/{week-1}')
        if not folder_path.exists():
            print('please wait while I generate your weekly breakdown for this day you requested.')
            self.createWeeklyBreakdown(name,str(month),str(week))
        file_path = folder_path/"breakdown.json" 
        with open(file_path, 'r') as file:
            data = json.load(file)
        temp_context = copy.deepcopy(self.context)
        for day in data[0]['days']:
            for subject in day['subjects']:
                
                instructions = f"I need you to create a **Lecture** for a {subject['subject_name']} student. The topic for today is {subject['subject_topic']}. Here are some sub_topics that should be covered this **Lecture** to compliment the main topic {subject['subject_daily_sub_topics']}. This should be your intro {subject['subject_daily_intro']}. This **Lecture** is student facing so it should always be addressing the student. There Should never be any notes for a speaker as the **lecutre** is going to be the speaking. After explaining a topic or subtopic fully pause then resume the lecture. Every time a pause should be represented as [p] It is important that you place [p] pauses after tackling subjects or topics. **wikipedia_refrences** should be given for most of the topics and sub topics. The **refrences** need to be put at the end with a key. I need about 60 - 90 minutes of **Lecture** material that will cover the main and sub topic, this should yeild a minimum word range of 1000 - 1400 words in the lecture. A **Summary** should be given talking about what the student has learned. Give the lecture a title, also at the very end display the main topic and sub topics."
                self.context.append({'role':'user', 'content' : instructions})

                fileName = f'{subject["subject_name"]}.json'
                GptUtil.makeJsonAPICall(self,Day,f'./data/yearPlan/{name}/weeklybreakdown/{month}/{week-1}/{day['day_name']}',fileName)
                self.context = copy.deepcopy(temp_context)
                subject_file_path = f'./data/yearPlan/{name}/weeklybreakdown/{month}/{week-1}/{day['day_name']}/{fileName}'
                subject_data = JsonUtil.get_students_specific_subject(subject_file_path)
                Parent.generateLectureQuestionsAndQuiz(self, subject_file_path, subject_data)
                print("fingers crossed")
        self.context = copy.deepcopy(temp_context)
        
    def createWeeklyQuiz(self, name: str, month: str, week: str,age : str, grade: str):
        folder_path = f'./data/yearPlan/{name}/weeklybreakdown/{month}/{int(week)-1}'
        data = JsonUtil.get_students_weekly_subjects_and_summaries(folder_path)
        temp_context = copy.deepcopy(self.context)
        for subject, summaries in data.items():
            self.context = copy.deepcopy(temp_context)
            intructions =  f"I need a end of week test for a {age} year old student. The **assumed_grade** is {grade} so please generate questions that range from one grade below and one grade above. The **subject_name** is {subject}, and there should be 20 questions that are based off these daily summaries ({summaries}) in that subject for that assumed grade. Each multiple choice question (**MCQ**) should follow this strict formating: - The **subject_name** should be displayed- **Question number** for each question header. - Display the **Grade level** of the question. - **Question** should be of a core topic in the subject. - **Options** should always be labeled with a number from 1)-4). - **Explanation** for the answer - **Answer** Should always start with the correct number option following the answer - **Subject Topic** the particular topic that this question covers. Another important note is never repeat the same question. Always double check to make sure you have not generated the same question."
            self.context.append({'role' : 'user', 'content' : intructions})
            GptUtil.makeJsonAPICall(self, WeeklyQuiz, folder_path, f'weekly_quiz.json')
        self.context = temp_context
        


    def testingChat(self, role = "user" ,test = "This is just a default test."):
        self.context.append({'role' : role, 'content' : test})
        GptUtil.makeChatAPICall(self)

    @staticmethod
    def calculateAssessmentNumber():
        folder_path = './data/assessments'
        os.makedirs(folder_path, exist_ok = True)
        files = os.listdir(folder_path)
        return len(files)
    
    @staticmethod
    def calculateYearPlanNumber(name:str):
        folder_path = f'./data/yearPlan/{name}'
        os.makedirs(folder_path,exist_ok=True)
        files = os.listdir(folder_path)
        return len(files)
    
    def testingO1(self, message:str):
        self.context.append({'role' : 'user', 'content' : message})
        GptUtil.makeJsonAPICallO1(self)
        
