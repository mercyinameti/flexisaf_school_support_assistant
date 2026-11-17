# models.py
# Defines the input shapes for each tool, with validation rules.

from pydantic import BaseModel, Field


class StudentLookupInput(BaseModel):
    student_id: str = Field(min_length=1, max_length=20, pattern=r"^S\d{3}$")


class GradeCalculatorInput(BaseModel):
    student_id: str = Field(min_length=1, max_length=20, pattern=r"^S\d{3}$")


class CourseSearchInput(BaseModel):
    keyword: str = Field(min_length=1, max_length=100)

class GradeChangeInput(BaseModel):
    student_id: str = Field(min_length=1, max_length=20, pattern=r"^S\d{3}$")
    course_code: str = Field(min_length=1, max_length=20, pattern=r"^[A-Z]{3}\d{3}$")
    new_score: int = Field(ge=0, le=100)