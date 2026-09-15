# Local service run and rollback handbook

as_of: 2026-09-15. Scope: fictional CPU demonstration only. Original documentation: CC BY-SA 4.0. Operator actions below are local and do not publish the book, expose a network service or contact another person.

## Start and inspect

Follow `code/part-ix/README.md` to create the declared environment and set `BOOK_PYTHON`. Start `"$BOOK_PYTHON" code/knowledge-assistant/service.py --port 0`. Record the exact returned URL, mode and state directory. The default temporary directory disappears on shutdown. For a deliberately retained synthetic store, pass `--state-dir /tmp/ka-local-demo-state`; record that directory's ownership and retention. Ctrl-C stops the owned service and workers. Do not kill unrelated preview processes.

Open the returned URL and check the current-date question, the complete source quotation and the historical date. Query the own order and verify that the interface identifies it as a fictional snapshot. A source result is not a live merchant confirmation. Use Stop on a new request, then check the stopped status. Prepare a handoff note and verify that it remains on screen; no sending action exists. Screen clearing and undo never alter a server request or order.

The command-line server intentionally has no administrative HTTP endpoint. For an observable local operator session, run this from the book root. The helpers use the same independently authored request/gate fixtures as the record runner:

```python
import json
import sys
sys.path[:0] = ["code/knowledge-assistant", "code/part-ix"]
from service import server
from support import submit

with server() as (app, url):
    job = submit(app, url)
    print(json.dumps(job.trace(), indent=2))
    print(json.dumps(app.monitor(), indent=2))
```

Only synthetic inputs belong in saved public traces. The ordinary diagnostic file omits question, result, principal and credential. A missing job after capacity eviction or restart is not proof that it never ran. The service is read-only, so no web request can have changed an order; that conclusion comes from its capability boundary, not from an absent log.

## Diagnose by first boundary

| Observation | Inspect first | Bounded action |
| --- | --- | --- |
| `401`, invalid body or forbidden host/origin | Credential mapping, exact fields, printed URL | Correct the local request; do not broaden authorization |
| `429` or `503` | Rate policy or active slots; include the rejection in eligible bad outcomes | Wait as indicated, reduce submissions, inspect running jobs; do not add unlimited retries |
| Progress stops but GET reports running | Connection state and retained job | Retrieve the existing ID; request cancellation if intended; do not resubmit blindly |
| `cancelled` | Cancellation event, stopped worker, no later terminal answer/cache publication | Verify the cancellation invariant; a connection close alone is insufficient |
| `dependency_unavailable` or circuit-open outcome | Attempt count, first failure and breaker state | Restore the injected dependency; wait cooldown; allow one probe |
| `deadline` | Total elapsed path and worker-stop event | Diagnose budget consumers; do not restart the full deadline for each retry |
| Correct JSON, wrong dated amount | Request date, effective date, source interval and captured manifest | Stop promotion, preserve trace and candidate, restore the accepted snapshot |
| Wrong source or missing answer report | Quarantined category and owned request | Maintainer reviews source facts, authors a minimized separate case and reruns old regressions |

The monitor is a bounded session view. Wait for active jobs to settle before treating its window as complete; also inspect `complete_window` and `dropped_records`. An alert describes the observed bad fraction, not its cause. Recovery does not remove earlier bad outcomes from the window.

## Release checklist and gate

The release owner performs these steps in the local exercise. The recorded run supplies machine-executed evidence, not an external human's approval signature.

1. Preserve source fixtures and independently authored expectations. Run the full applicable regression checks, including ownership, citation and cancellation behavior.
2. Create a manifest using `manifest()` or load a saved `rc-*.json`; verify current bytes using `verify_manifest`. Record runtime and scope. An altered executable needs a newly evaluated candidate, not a renamed old gate.
3. Evaluate each candidate on the same ten presentations using `release_gate`. The gate records expected and actual status, amount and source and binds its result to the manifest digest. A hard failure blocks normal `switch`.
4. Retain the accepted manifest, failing records, candidate and configuration compatibility statement. Choose cohort and stop conditions before switching. This demo sends every tenth accepted job to the canary; ten requests illustrate one candidate and nine controls, not statistical safety.
5. Inspect both cohorts and operational failures. Promote only the passing candidate within the declared local scope. Record the switch journal and all in-flight snapshots.
6. If the current-date answer becomes 600 or an authority invariant fails, stop further exposure and switch back to the retained accepted candidate. Recheck a new current request and account for jobs still carrying the old snapshot.

For a reviewable normal switch, after importing the modules above, use this explicit rapid-exercise instance:

```python
from service_ops import manifest, verify_manifest
from support import release_gate, submit

with server(rate=100, burst=100) as (app, url):
    accepted = manifest()
    candidate = manifest("rc-b", ttl=10)
    gate = release_gate(candidate)
    assert verify_manifest(candidate) and gate["passed"]
    app.release.switch(candidate, gate, canary=True)
    cohort = [submit(app, url).release["name"] for _ in range(10)]
    print(cohort)
    app.release.switch(candidate, gate)
    app.release.switch(accepted, release_gate(accepted))
    print(app.release.journal)
```

Use the explicitly declared higher rate for this ten-request routing exercise; it changes the experiment condition, not the default service policy. The executable `run_records.py` already performs this complete exercise with those values.

## Recorded rollback and recovery drill

Run `pnpm records:part-ix` in the clean environment to execute the controlled drill. It rejects `rc-stale` through the normal gate, then uses an explicitly labeled in-process `drill=True` to expose the fault locally. This bypass is not a release procedure. The actual record shows A and B each passing 10/10, stale passing 4/10, ordinary stale switch rejected, and a ten-request cohort with one B and nine A snapshots. A bad current-date request returns 600. After switching to A, a new request returns 750 while an already accepted stale job still returns 600.

Rollback is configuration-only: no code bytes or database schema changed. To restore a different executable in a future system, retain its actual artifact and dependency environment and verify data compatibility separately. Never claim that the current manifest-only switch performs those operations. It cannot undo a committed business effect.

The fault run separately injects a first-attempt failure that recovers, two failed requests that open the breaker, one no-attempt rejection, and one successful half-open probe after cooldown. Its five eligible jobs retain two good and three bad outcomes. The deadline, overload and rate-limit drills use separate declared instances. `policy-run.json` contains logical-clock arithmetic and must not be mislabeled as that measured timeline.

## Feedback, deletion and uncertain writes

The web API accepts only three categories tied to an owned completed request. It cannot approve, train from or publish feedback. `Feedback.review` is an in-process trusted-maintainer action: require a specific minimized request, independent expected value, source and rationale. The recorded review uses a fictional source-boundary case, then deletes the subject report. Do not copy private text into a public fixture merely because someone submitted it.

`cache.delete_subject((tenant,user))` and `feedback.delete_subject((tenant,user))` remove those in-memory rows; expiry and shutdown also apply. A complete real-user deletion request would need the operator to inventory job traces, backups, diagnostics and any exported evidence under its actual retention policy. The demo does not claim such a production erasure workflow. Never delete immutable public synthetic baselines in response to a fictional report.

For the separately tested approved-write CLI, a response lost after commit means `UNCERTAIN`. Preserve identity, exact approval, object version, original intent key and receipt. Reopen and reconcile that same intent; the recorded final effect count is one. Replay adds zero writes, and compensation requires manual review. The service UI has no order-write capability, so this recovery drill does not authorize web cancellation.
