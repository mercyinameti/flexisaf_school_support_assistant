# tool_schemas.py
# Describes each tool for the model: its name, purpose, and inputs.

TOOL_DECLARATIONS = [
    {
        "name": "search_courses",
        "description": "Find courses by a keyword in the course title or course code.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "Word to search for, such as 'Machine' or 'CSC'."}
            },
            "required": ["keyword"],
        },
    },
    {
        "name": "calculate_average",
        "description": "Calculate a student's average score across all their recorded courses.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string", "description": "Student ID in the form S followed by three digits, such as S001."}
            },
            "required": ["student_id"],
        },
    },
    {
        "name": "lookup_student",
        "description": "Return a student's name and level from their student ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string", "description": "Student ID in the form S followed by three digits, such as S001."}
            },
            "required": ["student_id"],
        },
    },
    {
        "name": "propose_grade_change",
        "description": "Propose changing a student's score in one course. This only records a proposal and needs approval before it takes effect.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {"type": "string", "description": "Student ID such as S001."},
                "course_code": {"type": "string", "description": "Course code such as CSC301."},
                "new_score": {"type": "integer", "description": "New score from 0 to 100."},
            },
            "required": ["student_id", "course_code", "new_score"],
        },
    },
]