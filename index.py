from controller.parentController import ParentController

pc = ParentController()

print("What age is your student?")
age = input()

print("What grade level or assumed grade level is your student?")
grade_level = input()


pc.assessmentTest(age,grade_level)
