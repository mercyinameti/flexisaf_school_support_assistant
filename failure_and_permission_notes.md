# Failure and permission-boundary notes

## Failures handled
- **Invalid input (422):** Pydantic rejects bad input before any tool runs. Examples: a student ID that isn't S plus three digits, an empty search keyword, and a score outside 0 to 100.
- **Not found (404):** An unknown student, or a student with no grades, returns 404 with a clear message.
- **Invalid state (400):** Approving a proposal twice, or approving one that was rejected, returns 400 and changes nothing.
- **Unknown tool:** `dispatch.py` returns an error message instead of running anything.

## Failures not handled
- **Name lookups:** `lookup_student` only accepts a student ID, so a question with a name can't be answered.
- **Model choosing the wrong tool:** Nothing checks that the model picked the right tool for the question. The validation only checks the inputs.
- **Data reset on restart:** Approved changes and pending proposals are held in memory, so a restart clears them.
- **Missing details in the audit log:** The log records the status code, not the inputs or the reason for a 400 or 404.

## Permission boundaries
- **The model can only read data and propose changes.** Approve and reject are not in the tool list, so the model can't call them.
- **Approval is a separate step.** A proposal only changes a grade after `/proposals/{id}/approve` is called.
- **No login.** Anyone who can reach the server can approve or reject a proposal. This is a gap for a real school system. It needs authentication before use.
- **No approver identity.** The audit log doesn't record who approved a change.
- **Changes are not written to the data file.** Approved changes live in memory only, so `school_data.json` is never altered.