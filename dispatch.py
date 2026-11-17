# dispatch.py
# Validates a model's tool call with its Pydantic model, then runs the matching tool.

from pydantic import ValidationError

import tools
from models import CourseSearchInput, GradeCalculatorInput, GradeChangeInput, StudentLookupInput

TOOLS = {
    "search_courses": (CourseSearchInput, tools.search_courses),
    "calculate_average": (GradeCalculatorInput, tools.calculate_average),
    "lookup_student": (StudentLookupInput, tools.lookup_student),
    "propose_grade_change": (GradeChangeInput, tools.propose_grade_change),
}


def run_tool_call(name, args):
    if name not in TOOLS:
        return {"error": f"Unknown tool: {name}"}
    input_model, function = TOOLS[name]
    try:
        validated = input_model.model_validate(args)
    except ValidationError as error:
        return {"error": "Invalid input", "details": error.errors(include_url=False, include_context=False)}
    return function(validated)