# Test results

| # | Scenario | Input | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | Valid lookup | `{"student_id": "S001"}` | 200, Ada Okafor | 200 | Pass |
| 2 | Unknown student | `{"student_id": "S999"}` | 404 | 404 | Pass |
| 3 | Invalid ID format | `{"student_id": "S12"}` | 422 | 422 | Pass |
| 4 | Valid average | `{"student_id": "S001"}` | 200, average 68.5 | 200 | Pass |
| 5 | Student with no grades | `{"student_id": "S004"}` | 404 | 404 | Pass |
| 6 | Course search | `{"keyword": "Machine"}` | 200, CSC305 | 200 | Pass |
| 7 | Empty keyword | `{"keyword": ""}` | 422 | 422 | Pass |
| 8 | Valid grade change proposal | S001, CSC301, new_score 80 | 200, pending_approval | 200 | Pass |
| 9 | Score out of range | S001, CSC301, new_score 150 | 422 | 422 | Pass |
| 10 | Approval rules | Approve P001; approve P001 again; reject P003; approve P003 | 200, 400, 200, 400 | 200, 400, 200, 400 | Pass |