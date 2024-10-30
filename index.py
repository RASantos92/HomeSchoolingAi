from controller.parent import Parent
pc = Parent()
def generateAssessmentTest():
    print("What age is your student?")
    age = input()

    print("What grade level or assumed grade level is your student?")
    grade_level = input()
    pc.assessmentTest(age,grade_level)

def generateYearlyPlan():
    print("Whats your students name?")
    name = input()
    
    print("What is your student's age?")
    age = input()
    
    
    print("How many subjects are you trying to create?")
    number_of_subjects = int(input())
    for i in range(number_of_subjects):
        print("Subjects Grade level?")
        grade_level = input()
        print(f"Please input the name of subject {i+1}")
        subject = input()
        pc.createYearlyLessonPlanForSubject(name,age,grade_level,subject)


print('What are you trying to accomplish? \n A) Assessment Test \n B) Generate Year Plan \n C) Create Weekly lesson plans for the whole year \n D) Generate Weekly Break down. \n E) Create Daily breakdown. \n F) test chat \n G) Short classes \n H) Generate weekly quiz') 

path = input().upper()

match path:
    case 'A':
        generateAssessmentTest()
    case 'B':
        generateYearlyPlan()
    case 'C':
        print("what is the students name?")
        name = input()
        pc.createWeeklyLessonPlanForStudent(name)
    case 'D':
        print("This requires your students name.")
        name = input()
        print("This also requires the month. \n USE THE NUMBER OF THE MONTH!! \n MM")
        month = input().capitalize()
        print("Last is the week number. \n For example 1,2,3,4. There are only ever 4 weeks of curriculum in each month")
        week_number = input()
        pc.createWeeklyBreakdown(name, month, week_number)
    case 'E':
        print("Whats your students name?")
        name = input()
        print("What is the month? \n USE THE NUMBER OF THE MONTH!! \n MM")
        month = input()
        print("what is the week number? \n This is going to be a number between 1-4 ")
        week = input()
        print("What day? \n Monday - Friday")
        day = input().capitalize()
        pc.createDailyBreakDown(name,month, week, day)
    case 'F':
        pc.testingChat("user", "can you provide me kid wiki links on Language arts, topic is Metaphors")
    case 'G':
        print("How many subjects are you needing to create?")
        number_of_subjects = input()
        print("What is the students name?")
        name = input()
        print("What is the students age?")
        age = input()
        for i in range(int(number_of_subjects)):
            print("What is the grade_level for this lesson plan?")
            grade_level = input()
            print("What is the subject for this lesson plan?")
            subject = input()
            print("what is the duration (in months) of the lesson plan?")
            duration = input()
            pc.createLessonPlanForSubject(name, age, grade_level, subject, duration)
    case 'H':
        print("What is the studnets name?")
        name = input()
        
        print("what is the month? \n MM!")
        month = input()
        
        print("what is the week number, example 1-4")
        week = input()
        
        print("what is the students age?")
        age = input()
        
        print("what is the students grade?")
        grade = input()
        
        pc.createWeeklyQuiz(name, month, week, age, grade)

