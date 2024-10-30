import json
import os
from pathlib import Path
class JsonDataCleaning:
    @staticmethod
    def retriveStudentsFullYearPlanAsDictionary(name:str):
        folder_path = Path(f"./data/yearPlan/{name}")
        os.makedirs(folder_path, exist_ok=True)
        all_data = []
        for json_file in folder_path.glob("*.json"):
            try:
                with open(json_file, 'r') as file:
                    data = json.load(file)
                    all_data.append(data)
                    print(f"Loaded data from {json_file}")
            except json.JSONDecodeError as e:
                print(f"Error reading {json_file}: {e}")
            except Exception as e:
                print(f"Unexpected error with {json_file}: {e}")
        usableData = {}
        for d in all_data:
            subject = d[0]["plan_subject"]
            for month in d[0]['months']:
                if month['month_name'] not in usableData:
                    usableData[month['month_name']] = {
                        subject :{
                                'topics' : month['topics'],
                                'monthly_subject_summary': month['summary']
                            } 
                        }
                else:
                    usableData[month['month_name']][subject] = {
                        'topics' : month['topics'],
                        'monthly_subject_summary': month['summary']
                    }
        return usableData
    
    @staticmethod
    def restructureAssessmentData(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        restructured_data = {}
        testSubjects = []
        # Loop through each question
        for subject in data:
            for question in subject['subjects']:
                subject = question['subject']
                # If the subject is not already in the dictionary, add it with an empty list
                if subject not in restructured_data:
                    restructured_data[subject] = []
                testSubjects.append(subject)
                # Append the question to the appropriate subject list
                restructured_data[subject].append({
                    "questionNumber": question['questionNumber'],
                    "question": question['question'],
                    "options": question['options'],
                    "explanation": question['explanation'],
                    "answer": question['answer'],
                    "grade_level": question['grade_level'],
                    "subject_topic": question['subject_topic']
                })
        print('*'*100, "\n",testSubjects)
        with open('./data/assessments/test.json', 'w') as file:
            json.dump(restructured_data, file, indent=4)
        print(f"Restructured data saved to {file_path}")