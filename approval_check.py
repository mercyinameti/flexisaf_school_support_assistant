from models import GradeChangeInput, GradeCalculatorInput
from tools import propose_grade_change, approve_change, reject_change, calculate_average

rejected = propose_grade_change(GradeChangeInput(student_id="S001", course_code="CSC301", new_score=80))
print(reject_change(rejected["proposal_id"]))
print(calculate_average(GradeCalculatorInput(student_id="S001")))

approved = propose_grade_change(GradeChangeInput(student_id="S001", course_code="CSC301", new_score=80))
print(approve_change(approved["proposal_id"]))
print(calculate_average(GradeCalculatorInput(student_id="S001")))