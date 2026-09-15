# Part IX dated implementation note

as_of: 2026-09-15. last_verified: 2026-09-14 for primary-source research and initial CPU/UI execution; final repository/browser verification is dated separately in [the validation record](part-ix-validation.md). Original documentation: CC BY-SA 4.0. All textbook additions remain draft. No service or website deployment was performed.

## Selected stack and compatibility

The tested interpreter is CPython 3.12.10, macOS 26.5.2 arm64. The official Python 3.12 documentation read during research displayed patch version 3.12.14; that is not the installed interpreter. `http.server.ThreadingHTTPServer` provides explicit loopback routes, `threading` provides state locks and cancellation events, and `subprocess` supplies a separately stoppable POSIX process group. `sqlite3` reuses the existing fictional tenant-aware order store. The inherited `jsonschema==4.25.1` enforces answer contracts. The exact fresh environment appears in `code/part-ix/requirements-tested.txt` and `data/part-ix/dependency-inventory.json`.

The notebook requirements inherit `nbformat==5.10.4`, `nbclient==0.10.2` and `ipykernel==6.30.1` from Part VII. This is an observed compatible installation, not a promise that every later transitive release or platform works. POSIX group termination is deliberate: an event flag alone cannot stop a worker blocked in arbitrary computation. Windows support and a Linux run remain unverified.

The website retains the existing Astro/Starlight/KaTeX stack and static figure renderer. The resolved package versions and lockfile belong to the repository; no UI framework or teaching interaction was added. The service UI uses native HTML labels/buttons, CSS focus, a polite status region and a small same-origin JavaScript client. Its strings are centralized in `data/knowledge-assistant/service-content-v1.json`.

## HTTP contract

Every request uses the actual printed `127.0.0.1` host and port. The handler rejects another Host, a mismatched supplied Origin, unsupported routes, non-JSON POSTs, transfer encoding, duplicate/unknown JSON fields, non-finite values and oversized bodies. Input is bounded to 4,096 bytes and questions to 500 characters. Demo authentication is a fixed host mapping; supplying identity in the request body is invalid. These restrictions narrow the exercise; the standard-library server is explicitly not a production server.

| Operation | Contract |
| --- | --- |
| `POST /api/requests` | Exact fields `question`, `on_date`, `topic`, `locale`; topics `travel`, `approval`, `order`; language `en` or `zh-hans`; valid ISO date; order question is an order ID. Returns `202` and request ID, or a typed rejection |
| `GET /api/requests/{id}` | Reauthorize ownership; retrieve state and final result if present; another owner receives `404` |
| `GET /api/requests/{id}/events` | Reauthorize ownership; UTF-8 `text/event-stream`, numeric event IDs, JSON data, blank-line frame boundary; optional numeric `Last-Event-ID` resumes retained events |
| `POST /api/requests/{id}/cancel` | Empty object; `202` sets stopping intent before terminal state, `409` if already terminal; no order mutation |
| `POST /api/requests/{id}/feedback` | Exact category in `wrong_source`, `missing_answer`, `hard_to_use`; own terminal request; returns quarantined report |

Progress frames are not unverified answer tokens. The fetch reader implements only the subset emitted here, not a complete EventSource implementation. Dropping a stream does not cancel work. It may leave completion unknown to the client. Final-result GET can be retried within the client bound; job-creation POST is not automatically repeated. The UI shows a plain interruption state rather than claiming failure or undo.

## Operational values and interpretation

Default assigned values are two active jobs, three seconds of total server budget, at most two dependency attempts, 0.05 seconds between attempts, and a 0.05-second demonstration work delay. There is no pending-work queue. The user bucket starts at four tokens and refills at two per second. Excess input gets `429`; unavailable active capacity gets `503`. No attempt can reset the original deadline. Cancellation and timeout stop the child process group before completion bookkeeping releases the active slot.

Response cache capacity is 64; the default candidate uses a 30-second TTL and candidate B uses 10. The key covers host tenant/user/scopes, complete request and release digest. Authorization precedes lookup. A cache entry expires at or after its boundary; maintenance also removes expired rows. Orders are never response-cached. Semantic caching is disabled following the fixed false-match example. The breaker counts consecutive failed requests after bounded attempts; two open it for 0.25 seconds. One half-open probe is allowed. Cancellation releases a probe without counting a dependency failure.

The monitor uses server-observed eligible submissions in a half-open interval `[start,end)`, excluding acknowledged cancellations from the availability denominator and separately counting invalid/unauthenticated requests. Answered/abstained/refused outcomes within the deadline are operationally good; content quality is measured separately. Errors, rate limiting and overload are bad eligible outcomes. The assigned SLO is 95%; a demonstration alert needs at least five eligible outcomes and a bad fraction strictly greater than twice the allowed 5%. This is not a recommended production alert configuration. Metrics retain at most 1,000 rows; truncation explicitly marks the session window incomplete. In-flight jobs have not yet emitted a terminal outcome, so the snapshot is provisional until they settle.

Job retention is at most 100 records, evicting completed work to accept new work. A restart loses jobs, cache, monitor and feedback state. Feedback holds at most 100 categorical reports, logically expires at seven days and is physically swept approximately once per second; shutdown discards it. Diagnostics rotate at approximately one million bytes with one prior file, omit sensitive content, and have no independent wall-clock deletion policy. A supplied state directory retains diagnostics and the fictional SQLite store until the operator removes that directory. Default temporary state is cleaned at shutdown.

## Deliberate limits

The release manager switches compatible configuration snapshots inside one unchanged running executable. Its hash verifier detects changed current source bytes; it does not store those bytes or restore an executable, operating system or data migration. The in-process operator is trusted and can explicitly bypass a gate only for the labeled local fault drill. There is no remote release API, identity administration or feedback review API.

Trace IDs and span relationships borrow the stable tracing model. These are local JSON records, not OpenTelemetry SDK/OTLP integration. Historical model, tokenizer and protocol details remain in Parts VI–VIII dated notes; Part IX makes zero new neural calls. The retained read-only MCP teaching subset is not promoted to a full protocol SDK or connected to a real merchant system. The bibliography and supported sections are in [the research ledger](part-ix-research.md).
