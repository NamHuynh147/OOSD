# Test plan

| Area | Coverage |
| --- | --- |
| Tool policy | Reject any tool name outside the allowlist |
| Budget guard | Stop before step/token/time limits are exceeded |
| Injection guard | Flag known instruction-override patterns without flagging ordinary policy text |
| Tool surface | Keep adapters behind the `ReadOnlyTool` interface; HTTP adapter accepts GET only |
| Evidence | Keep evidence frozen and append-only; preserve content hashes and stable citation IDs |
| Orchestrator | Exercise planning, guarded tool calls, report citation validation, and partial results after cancellation |
| API | Validate create/read/cancel flows, configured maximum budgets, and 404 handling |

Run the backend suite with `cd backend; pytest`. Add database integration tests with a disposable PostgreSQL service before deploying.
