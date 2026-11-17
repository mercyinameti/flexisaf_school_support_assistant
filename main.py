# main.py
# Exposes the school tools and the approval actions as FastAPI endpoints.

import json
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request

import tools
from models import CourseSearchInput, GradeCalculatorInput, GradeChangeInput, StudentLookupInput

app = FastAPI(title="School Support Assistant")

AUDIT_FILE = "audit_log.jsonl"
NOT_FOUND_MESSAGES = ("not found", "No grade", "no longer exists")


@app.middleware("http")
async def audit_requests(request: Request, call_next):
    response = await call_next(request)
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")
    return response


def check_result(result):
    # Turns a tool's error message into an HTTP error code.
    if isinstance(result, dict) and "error" in result:
        code = 404 if any(text in result["error"] for text in NOT_FOUND_MESSAGES) else 400
        raise HTTPException(status_code=code, detail=result["error"])
    return result


@app.post("/tools/search-courses")
def search_courses(data: CourseSearchInput):
    return check_result(tools.search_courses(data))


@app.post("/tools/calculate-average")
def calculate_average(data: GradeCalculatorInput):
    return check_result(tools.calculate_average(data))


@app.post("/tools/lookup-student")
def lookup_student(data: StudentLookupInput):
    return check_result(tools.lookup_student(data))


@app.post("/tools/propose-grade-change")
def propose_grade_change(data: GradeChangeInput):
    return check_result(tools.propose_grade_change(data))


@app.get("/proposals")
def list_proposals():
    return tools.PENDING_CHANGES


@app.post("/proposals/{proposal_id}/approve")
def approve(proposal_id: str):
    return check_result(tools.approve_change(proposal_id))


@app.post("/proposals/{proposal_id}/reject")
def reject(proposal_id: str):
    return check_result(tools.reject_change(proposal_id))