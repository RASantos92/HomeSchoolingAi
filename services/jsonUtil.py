from pathlib import Path
import json
import os
class JsonUtil:
    @staticmethod
    def saveModelToJsonFile(model, folderPath, fileName):
        modelJson = model.model_dump_json()
        
        folderPath = Path(folderPath)
        filePath = folderPath/fileName
        if not filePath.exists() or  filePath.stat().st_size == 0:
            data = []
        else:
            with open(filePath, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        print(type(data), type(data) == 'dict')
        if type(data) == dict:
            data = [data]
        data.append(json.loads(modelJson))
        os.makedirs(folderPath, exist_ok=True)
        
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=4)
            print(f'updated {filePath}')
    
    @staticmethod
    def getStudentsWeeklyPlan(name:str) -> object:
        folder_path = Path(f'./data/yearPlan/{name}/weeklyPlans')
        if not folder_path.exists:
            print('You need to create a weekly Plan for the year first for your student first.\n That is option C)')
            return None
        with open(folder_path/"weeklyPlans.json", 'r') as file:
            data = json.load(file)
        return data
    
    # Function to initialize the JSON structure if it doesn't exist
    @staticmethod
    def initialize_progress_file(progress_file_path):
        """Creates a default structure for weekly_progress.json."""
        initial_data = {
            "Monday": {},
            "Tuesday": {},
            "Wednesday": {},
            "Thursday": {},
            "Friday": {}
        }
        # Save the structure to the file
        with open(progress_file_path, "w") as file:
            json.dump(initial_data, file, indent=4)
    
    @staticmethod
    def get_weekly_progress_file(name, month, week, day):
        progress_file_path = Path(f'./data/yearPlan/{name}/weeklyBreakdown/{month}/{week}/{day}/weekly_progress.json')
        # Ensure the parent directories exist
        progress_file_path.parent.mkdir(parents=True, exist_ok=True)

        # If the file doesn't exist, initialize it with the default structure
        if not progress_file_path.exists():
            JsonUtil.initialize_progress_file(progress_file_path)

        return progress_file_path
    
    # Function to update progress for the current day
    @staticmethod
    def update_progress(name, month, week, day, data, subject):
        """Updates the progress for a given day."""
        # Get the progress file path (creates the file if necessary)
        progress_file_path = JsonUtil.get_weekly_progress_file(name, month, week, day )

        # Load the current progress data
        with open(progress_file_path, "r") as file:
            progress_data = json.load(file)

        # Update the day's progress with the new data
        if subject in progress_data[day]:
            progress_data[day][subject].append(data)
        else:
            progress_data[day][subject] = [data]

        # Save the updated progress back to the file
        with open(progress_file_path, "w") as file:
            json.dump(progress_data, file, indent=4)
            
            
    @staticmethod
    def get_students_weekly_subjects_and_summaries(Folder_path):
        path = Path(Folder_path)
        data = {}

        for day_folder in path.iterdir():
            if day_folder.is_dir():
                for subject_file in day_folder.iterdir():
                    if subject_file.suffix == '.json':
                        subject_name = subject_file.stem
                        
                        # Load the JSON file to extract the sub_topics
                        with open(subject_file, 'r') as f:
                            subject_data = json.load(f)
                            summary = subject_data[0]["lessons"][0].get('summary', "")
                        if subject_name not in data: 
                            data[subject_name] = summary
                        else:
                            data[subject_name] = data[subject_name] + ", \n " + summary
        return data
    
    @staticmethod
    def get_students_specific_subject(file_path):
        subject_file_path = Path(file_path)
        with open(subject_file_path, 'r') as f:
            subject_data = json.load(f)
            output = subject_data[0]["lessons"][0]
        return output

