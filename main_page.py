import streamlit as st
from pathlib import Path
import json
from datetime import datetime
from controller.parent import Parent
from streamlit.components.v1 import html
from services.jsonUtil import JsonUtil

pc = Parent()

# # Define the base path to the yearPlan directory using Path from pathlib
# base_path = Path('./data/yearPlan/Hayden/weeklyBreakdown')
# # Get the current month (e.g., 09 for September)
# current_month = datetime.now().strftime('%m')
# # Get the current day of the week (e.g., Monday)
# current_day = datetime.now().strftime('%A')
# # Get the current week of the month (week number 1 to 4)
# today = datetime.now()
# week_number = (today.day - 1) // 7 + 1  # Weeks start at 1 instead of 0
# # Construct the path to the current week's folder (month -> week -> day)
# # current_week_folder = base_path / current_month / str(week_number-1) / current_day
# # Having to use while in beta, Hard coded date
# current_week_folder = base_path / "09" / str(2) / "Tuesday"

# Define the months (08 through 05) excluding summer break (06 and 07)
months = ['08', '09', '10', '11', '12', '01', '02', '03', '04', '05']

# Define the weeks as 0 to 3 for each month
weeks = ['0', '1', '2', '3']

# Sidebar for selecting the month and week
selected_month = '11'
selected_week = '0'

# Define days of the week
days_of_week = ['Wednesday']
selected_day = st.sidebar.selectbox("Choose a day", days_of_week)

# Construct the base path to the selected month and week
base_path = Path(f'./data/yearPlan/Hayden/weeklyBreakdown/{selected_month}/{selected_week}')
day_folder_path = base_path / selected_day  # Dynamically use the selected day

# Check if the day folder exists and list subject JSON files
if day_folder_path.exists():
    subject_files = [f.name for f in day_folder_path.iterdir() if f.suffix == '.json']
else:
    st.sidebar.write("No data available for the selected day.")
    subject_files = []

if 'close' not in st.session_state:
    st.session_state["close"] = False
if 'quiz_close' not in st.session_state:
    st.session_state['quiz_close'] = False
if 'selected_subject' not in st.session_state:
    st.session_state['selected_subject'] = None
if 'user_lecture_answers' not in st.session_state:
    st.session_state['user_lecture_answers'] = {}
if "wrong_answer_indexes" not in st.session_state:
    st.session_state['wrong_answer_indexes'] = {}
if "correct_answers" not in st.session_state:
    st.session_state['correct_answers'] = 0
if 'wrong_quiz_answer_indexes' not in st.session_state:
    st.session_state['wrong_quiz_answer_indexes'] = {}
if 'quiz_view' not in st.session_state:
    st.session_state['quiz_view'] = False
if 'quiz_grade' not in st.session_state:
    st.session_state['quiz_grade'] = 0
if "lecture_grade" not in st.session_state:
    st.session_state['lecture_grade'] = 0
if "quiz_attempts" not in st.session_state:
    st.session_state['quiz_attempts'] = 0
if "final_attempt" not in st.session_state:
    st.session_state['final_attempt'] = False
if "highest_grade" not in st.session_state:
    st.session_state['highest_grade'] = 0
# Initialize session state for the selected video index
if 'selected_video' not in st.session_state:
    st.session_state['selected_video'] = None  # No video selected initially
    
# Function to update the selected video in the session state
def select_video(index):
    st.session_state['selected_video'] = index

def inject_scroll_script():
    scroll_script = """
    <script>
        function scrollToTop() {
            var body = window.parent.document.querySelector('.main');
            body.scrollTo(0, 0);
        };
        scrollToTop();
    </script>
    """
    # Inject the script into Streamlit's frontend
    st.components.v1.html(scroll_script, height=0)
    
def toggle_start_quiz():
    st.session_state['quiz_view'] = not st.session_state['quiz_view']
    inject_scroll_script()
    
def toggle_final_attempt():
    with open(subject_file_path, 'r') as file:
        lecture_data = json.load(file)
    # Update the first object in the array
    if 'complete' not in lecture_data[0]:
        lecture_data[0]['complete'] = True
    else:
        lecture_data[0]['complete'] = True
    # Write the updated data back to the JSON file
    with open(subject_file_path, 'w') as file:
        json.dump(lecture_data, file, indent=4)
    st.session_state['final_attempt'] = True

daily_youtube_videos = ["https://www.youtube.com/watch?v=Xc4xYacTu-E", "https://www.youtube.com/watch?v=J51ncHP_BrY"]
# Create a navigation bar with buttons for each video
st.sidebar.header("Video Navigation")
for i, video_url in enumerate(daily_youtube_videos):
    st.sidebar.button(f"Video {i+1}", on_click=select_video, args=(i,))
# Display the selected video using an iframe at the top of the page
if st.session_state['selected_video'] is not None:
    selected_video_url = daily_youtube_videos[st.session_state['selected_video']]
    st.markdown(
        f"""
        <iframe width="800" height="450" 
        src="{selected_video_url}&playsinline=1" 
        frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen></iframe>
        """, 
        unsafe_allow_html=True
    )

if subject_files:
    st.sidebar.write("Subjects:")
    for subject_file in subject_files:
        subject_file_path = day_folder_path / subject_file
        with open(subject_file_path, 'r') as file:
                lecture_data = json.load(file)
            # Check if the subject is complete
        if subject_file_path.stem == 'weekly_progress':
            continue
        if lecture_data and 'complete' in lecture_data[0]:
            # Green background for completed subjects
            st.sidebar.markdown(
                f"<div style='background-color: #90EE90; padding: 10px; margin-bottom: 5px;'>{subject_file.split('.')[0]}</div>",
                unsafe_allow_html=True
            )
        else:
            # Default background for incomplete subjects
            st.sidebar.markdown(
                f"<div style='background-color: #FFCCCB; padding: 10px; margin-bottom: 5px;'>{subject_file.split('.')[0]}</div>",
                unsafe_allow_html=True
            )
            if st.sidebar.button(f"Open {subject_file.split('.')[0]}"):
                st.session_state['selected_subject'] = subject_file_path
                del st.session_state['quiz_grade']
                del st.session_state['lecture_grade']
                st.session_state['quiz_view'] = False
                st.rerun()

if st.session_state['selected_subject']:
    # Path to the selected subject's JSON file
    subject_file_path = st.session_state['selected_subject']
    with open(subject_file_path, 'r') as file:
        lecture_data = json.load(file)
    # Dictionary to hold user's answers
    user_lecture_answers = {}
    # Flag to check if the test has been submitted
    submitted = st.session_state.get('lecture_submitted', False)
    wrong_answers_lecture_questions = []
    # Display the lecture content
    
    for lesson in lecture_data[0].get("lessons", []):
        # This will generate a quiz for the lecture if it is not already created
        if 'quiz' not in lesson:
            # here we need to make a call to generate the quiz and update the lectures file path
            lesson = pc.generateLectureQuestionsAndQuiz(subject_file_path,lesson)
        # Spliting the lecture at the pauses.
        st.title(f"{subject_file_path.stem}")
        lecture_chapters = lesson['lecture'].split("[p]")
        # Obtaining the total amount of questions for the lecture questions
        st.session_state['total_lecture_questions'] = len(lesson['lecture_questions'])
        # Here we loop through the chapters of the lectures.
        # Display lecture details
        if not st.session_state.get('quiz_view', False):
            st.subheader("Lecture")
            for index, chapter in enumerate(lecture_chapters):
                st.markdown(rf"""
                            <p>{chapter}<p>
                            """
                            , unsafe_allow_html=True)

            lecture_questions = lesson['lecture_questions']
            st.write(f"Lecture Questions:")
            for index, question in enumerate(lecture_questions):
                st.write(question['question'])
                # This checks if the question has been answered wrong, if the student is close then we display that this is the question that was wrong.
                if index in st.session_state['wrong_answer_indexes'] and st.session_state['close']:
                    st.markdown(f'<p style="color:red;">{st.session_state["wrong_answer_indexes"][index]}<p>', unsafe_allow_html=True)
                # displaying the options for the question for the student.
                user_lecture_answers[index] = st.radio(
                    f"Select answer for the question:",
                    options = question['options'],
                    key=f"question_{index}"
                )

            # st.write(chapter_question['answer'])
            # Submission of the lecture questions
            if st.button("Submit Lecture Questions"):
                correct_answers = 0
                for index, question in enumerate(lesson['lecture_questions']):
                    if user_lecture_answers[index][0] == question['answer'][0]:
                        if index in st.session_state['wrong_answer_indexes']:
                            del st.session_state['wrong_answer_indexes'][index]
                        correct_answers += 1
                    else:
                        st.session_state['wrong_answer_indexes'][index] = "The answer to this questions is wrong."
                        wrong_answers_lecture_questions.append(index)
                st.session_state['lecture_submitted'] = True
                st.session_state['correct_answers'] = correct_answers
                st.session_state['lecture_grade'] = round((correct_answers / st.session_state['total_lecture_questions']) * 100,2)
                st.session_state['number_of_wrong_answers_lecture_questions'] = len(wrong_answers_lecture_questions)

    # This will inform the student that about their grade on the lecture questions,
    if not st.session_state['quiz_view']:
        # If the student is below passing let them know they are far from 100%,
        # Otherwise inform the student they are close.
        if st.session_state['lecture_grade'] == 100:
            if st.session_state.get('quiz_view', False):
                st.write("Good Luck on the test!!")
                st.button("Review Lecture", on_click=toggle_start_quiz)
            else:
                st.write("Awesome job. 100% correct!")
                st.button("Attempt Quiz", on_click=toggle_start_quiz)
        elif st.session_state['lecture_grade'] >= 70:
            st.write("You are close to 100%! You need 100% to take the quiz and move on.")
            st.session_state['close'] = True
        elif st.session_state['lecture_grade'] > 0:
            st.write("You are far from 100%. You need 100% to take the quiz and move on.")
            st.session_state['close'] = False

    # If the student has a passing grade for the lecture questions 
    if  st.session_state.get('quiz_view',False) and not st.session_state.get('final_attempt'):
        st.subheader("Quiz Time")
        # This will store the students quiz answers
        user_quiz_answers = {}
        wrong_answers_quiz_questions = []
        submitted_quiz = st.session_state.get('quiz_submitted', False)
        st.session_state['correct_answers'] = 0
        st.session_state["total_questions_quiz_questions"] = len(lesson['quiz'])
        st.header("Quiz:")
        # Loop through the lesson quiz to display the questions to the student and record their answers.
        for index, question in enumerate(lesson['quiz']):
            st.write(f"Question {index}: \n {question['question']}")
            if index in st.session_state['wrong_quiz_answer_indexes'] and st.session_state['quiz_close']:
                st.markdown(f'<p style="color:red;">{st.session_state["wrong_quiz_answer_indexes"][index]}<p>', unsafe_allow_html=True)
            user_quiz_answers[index] = st.radio(
                f"Select answer for question {index}:",
                options = question['options'],
                key=f"quiz_question_{index}"
            )

        if st.button("Submit Quiz"):
            correct_answers = 0
            for index, question in enumerate(lesson['quiz']):
                if user_quiz_answers[index][0] == question['answer'][0]:
                    print("here")
                    if index in st.session_state['wrong_quiz_answer_indexes']:
                        del st.session_state['wrong_quiz_answer_indexes'][index]
                    correct_answers += 1
                else:
                    st.session_state['wrong_quiz_answer_indexes'][index] = "This answer is incorrect"
                    wrong_answers_quiz_questions.append(index)
            st.session_state['quiz_submitted'] = True
            st.session_state['correct_answers'] = correct_answers
            st.session_state['quiz_grade'] = round((correct_answers / st.session_state['total_questions_quiz_questions'])*100,2)
            st.session_state['wrong_answers_quiz_questions'] = (st.session_state.get("wrong_answers_quiz_questions", 0) + len(wrong_answers_quiz_questions))
            st.session_state['quiz_attempts'] += 1
            st.session_state['highest_grade'] = round((correct_answers / st.session_state['total_questions_quiz_questions'])*100,2) if round((correct_answers / st.session_state['total_questions_quiz_questions'])*100,2) > st.session_state['highest_grade'] else st.session_state['highest_grade']
            data = {
                "quiz_grade" : round((correct_answers / st.session_state['total_questions_quiz_questions'])*100,2),
                "wrong_answers" : wrong_answers_quiz_questions,
                "attempt_number": st.session_state['quiz_attempts'] + 1,
                "quiz" : lesson['quiz']
            }
            JsonUtil.update_progress("Hayden", selected_month, selected_week, selected_day, data,subject_file_path.stem)
            if (st.session_state['quiz_attempts'] +1) > 3: 
                toggle_final_attempt()

        # Display the quiz grade to the student.
        if 'quiz_grade' in st.session_state:
            if st.session_state['quiz_grade'] == 100:
                with open(subject_file_path, 'r') as file:
                    lecture_data = json.load(file)
                
                # Update the first object in the array
                if 'complete' not in lecture_data[0]:
                    lecture_data[0]['complete'] = True
                else:
                    lecture_data[0]['complete'] = True
                
                # Write the updated data back to the JSON file
                with open(subject_file_path, 'w') as file:
                    json.dump(lecture_data, file, indent=4)

                st.write("Marked as complete!")
                st.write('Awesome job. You finised the quiz with a 100%')
                st.write(st.session_state['wrong_answers_quiz_questions'])
                # Display summary
                st.subheader("Summary")
                st.write(lesson.get("summary", "No summary available"))
            elif st.session_state['quiz_grade'] >= 70:
                st.write("You are close to 100%, keep going!")
                st.session_state['quiz_close'] = True
            else:
                st.write(f"You are far off from 100%")
                st.session_state['quiz_close'] = False
            # st.write(st.session_state['quiz_grade'])
    if st.session_state['final_attempt']:
        st.title("That was your final attempt at the quiz")
        st.subheader(f"Your best quiz score was a {st.session_state['quiz_grade']}%")
        st.button("Review Lecture", on_click=toggle_start_quiz)
    
        # Display Wikipedia references
        st.subheader("Wikipedia References")
        for reference in lesson.get("wikipedia_refrences", []):
            st.write(f"- ({reference})")
