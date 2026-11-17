# School Support Assistant

A tool-using assistant for common school tasks. It answers questions by calling three read-only tools, and it can propose a grade change that waits for approval before it takes effect.

## Setup

1. Create a virtual environment with Python 3.12:
   `py -3.12 -m venv .venv`
2. Activate it:
   `.venv\Scripts\Activate.ps1`
3. Install the packages:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and replace `your-key-here` with your Gemini API key.

## Running the server

`uvicorn main:app --reload`

Then open `http://127.0.0.1:8000/docs` to try each endpoint.

## Asking the assistant

`python ask_model.py "What is the average score for student S001?"`

The model picks a tool and fills in its inputs. The tool runs only if its inputs pass validation.

## Tools

- `search_courses`: finds courses by a keyword in the title or code.
- `calculate_average`: calculates a student's average across their courses.
- `lookup_student`: returns a student's name and level from their ID.
- `propose_grade_change`: records a proposed grade change. It doesn't change any data.

## Approval

A proposed change takes effect only when `/proposals/{id}/approve` is called. Rejecting a proposal with `/proposals/{id}/reject` leaves the data unchanged. The model can't approve or reject changes.

## Data

`school_data.json` is mock data made up for testing. Approved changes are held in memory and reset when the server restarts.

## Files

- `models.py`: Pydantic input models.
- `tools.py`: the tool functions and the approval actions.
- `tool_schemas.py`: the tool descriptions the model reads.
- `dispatch.py`: validates a tool call, then runs the matching tool.
- `ask_model.py`: sends a question to Gemini and runs the tool it chooses.
- `main.py`: FastAPI endpoints and the audit log.
- `audit_log.jsonl`: one line per request, with the time, method, path, and status.

## Documentation

- `test_results.md`: the test scenarios and results.
- `failure_and_permission_notes.md`: failures handled, failures not handled, and permission boundaries.