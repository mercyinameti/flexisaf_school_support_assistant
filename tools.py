# tools.py
# Read-only tools for course search, grade average, and student lookup.

import json
from pathlib import Path

from models import CourseSearchInput, GradeCalculatorInput, GradeChangeInput, StudentLookupInput

DATA = json.loads(Path("school_data.json").read_text(encoding="utf-8"))


def search_courses(data: CourseSearchInput) -> list[dict]:
    keyword = data.keyword.lower()
    return [
        course for course in DATA["courses"]
        if keyword in course["title"].lower() or keyword in course["course_code"].lower()
    ]


def calculate_average(data: GradeCalculatorInput) -> dict:
    scores = [g["score"] for g in DATA["grades"] if g["student_id"] == data.student_id]
    if not scores:
        return {"student_id": data.student_id, "error": "No grades found for this student."}
    return {
        "student_id": data.student_id,
        "average": round(sum(scores) / len(scores), 1),
        "courses_counted": len(scores),
    }


def lookup_student(data: StudentLookupInput) -> dict:
    for student in DATA["students"]:
        if student["student_id"] == data.student_id:
            return student
    return {"student_id": data.student_id, "error": "Student not found."}

PENDING_CHANGES = {}


def propose_grade_change(data: GradeChangeInput) -> dict:
    current = next(
        (g for g in DATA["grades"]
         if g["student_id"] == data.student_id and g["course_code"] == data.course_code),
        None,
    )
    if current is None:
        return {"error": "No grade record found for this student and course."}
    proposal_id = f"P{len(PENDING_CHANGES) + 1:03d}"
    PENDING_CHANGES[proposal_id] = {
        "student_id": data.student_id,
        "course_code": data.course_code,
        "old_score": current["score"],
        "new_score": data.new_score,
        "status": "pending_approval",
    }
    return {"proposal_id": proposal_id, **PENDING_CHANGES[proposal_id]}

def approve_change(proposal_id: str) -> dict:
    change = PENDING_CHANGES.get(proposal_id)
    if change is None:
        return {"error": "Proposal not found."}
    if change["status"] != "pending_approval":
        return {"error": f"Proposal is already {change['status']}."}
    for grade in DATA["grades"]:
        if grade["student_id"] == change["student_id"] and grade["course_code"] == change["course_code"]:
            grade["score"] = change["new_score"]
            change["status"] = "approved"
            return {"proposal_id": proposal_id, "status": "approved", "score": grade["score"]}
    return {"error": "Grade record no longer exists."}


def reject_change(proposal_id: str) -> dict:
    change = PENDING_CHANGES.get(proposal_id)
    if change is None:
        return {"error": "Proposal not found."}
    if change["status"] != "pending_approval":
        return {"error": f"Proposal is already {change['status']}."}
    change["status"] = "rejected"
    return {"proposal_id": proposal_id, "status": "rejected"}