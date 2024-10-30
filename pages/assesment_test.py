import streamlit as st
import pandas as pd
import numpy as np
import json
# st.title("Just learning how to use forms in streamlit")

# st.markdown("# Main page 🎈")
# st.sidebar.markdown("# Main page 🎈")

with open('./data/assessments/assessment15.json', 'r') as file:
    data = json.load(file)

questions = [d.get("subjects", []) for d in data]
main_subjects = [ l[0]['subject'] for l in questions]

subject_selection = st.sidebar.selectbox("Choose a subject", main_subjects)

selected_subject = None
for list_of_questions in questions:
    if list_of_questions[0].get("subject") == subject_selection:
        selected_subject = list_of_questions
        break
    
# Dictionary to hold user's answers
user_answers = {}
# Flag to check if the test has been submitted
submitted = st.session_state.get('submitted', False)
wrong_answers = []
if "correct_answers" not in st.session_state and "total_questions" not in st.session_state:
    st.session_state['correct_answers'] = 0
    st.session_state['total_questions'] = 10
if selected_subject:
    st.title(f"Test for {selected_subject[0].get('subject')}")

    # Only render questions if the test has not been submitted yet
    if not submitted:
        for index, question_data in enumerate(selected_subject):
            st.write(f"Question {index + 1}: {question_data['question']}")
            
            # Use the question index as the unique key for each set of radio buttons
            user_answers[index] = st.radio(
                f"Select answer for question {index + 1}:",
                options=question_data['options'],
                key=f"question_{index}"
            )
        
        # Submit button
    if st.button("Submit"):
            correct_answers = 0
            total_questions = len(selected_subject)

            for index, question_data in enumerate(selected_subject):
                # Compare user's answer with the correct answer
                if user_answers[index] == question_data['answer']:
                    correct_answers += 1
                else:
                    wrong_answers.append(question_data['subject_topic'])
            
            # Store submission state in session_state
            st.session_state['submitted'] = True
            st.session_state['correct_answers'] = correct_answers
            st.session_state['total_questions'] = total_questions
            st.write(f"You got {correct_answers} out of {total_questions} correct!")
    else:
        # If already submitted, show score
        correct_answers = st.session_state['correct_answers']
        total_questions = st.session_state['total_questions']
        st.write(f"You got {correct_answers} out of {total_questions} correct!")
        st.write(f"Your score: {(correct_answers / total_questions) * 100:.2f}%")

# Custom CSS to reduce the padding between the radio buttons
st.markdown("""
    <style>
    .stRadio > div {
        gap: 10px;  /* Decrease this to reduce the spacing */
    }
    </style>
""", unsafe_allow_html=True)