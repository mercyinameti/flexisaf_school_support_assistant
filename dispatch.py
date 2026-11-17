# dispatch.py
# Validates a tool call with its Pydantic model, runs the matching tool, and records the attempt.

from pydantic import ValidationError

import tools
from audit import record_tool_attempt
from models import CourseSearchInput, GradeCalculatorInput, GradeChangeInput, StudentLookupInput

TOOLS = {
    "search_courses": (CourseSearchInput, tools.search_courses),
    "calculate_average": (GradeCalculatorInput, tools.calculate_average),
    "lookup_student": (StudentLookupInput, tools.lookup_student),
    "propose_grade_change": (GradeChangeInput, tools.propose_grade_change),
}


def run_tool_call(name, args, source="model"):
    if name not in TOOLS:
        record_tool_attempt(name, source, "unknown_tool")
        return {"error": f"Unknown tool: {name}"}
    input_model, function = TOOLS[name]
    try:
        validated = input_model.model_validate(args)
    except ValidationError as error:
        record_tool_attempt(name, source, "invalid_input")
        return {"error": "Invalid input", "details": error.errors(include_url=False, include_context=False)}
    result = function(validated)
    outcome = "error" if isinstance(result, dict) and "error" in result else "ok"
    record_tool_attempt(name, source, outcome)
    return result