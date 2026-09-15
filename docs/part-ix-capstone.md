# KA-10 capstone handover and evaluation report

as_of: 2026-09-15. Original documentation: CC BY-SA 4.0. Decision: accept the evidenced, local, fictional, read-only demonstration scope. Do not claim public production readiness, broad paraphrase quality or a newly validated neural answer generator. All Chapter 54–57 pages and the existing HTTP Primer remain drafts. No commit, push, publication or deployment is part of this handover.

## Requirements and threat boundary

The reader asks for a dated fictional Beijing lodging policy with an exact quotation, or reads an owned fictional order. Current policy is 750 yuan per room per night from 2026-01-01; the retained 2025 interval is 600. Missing evidence must lead to abstention, and failed authorization must not reveal another principal's record. A request may be stopped without a late answer being published. Release identity, bounded failures, recovery and feedback review must be inspectable.

Host identity, reviewed local code and the local operator are trusted. Questions, evidence text, tool results and Skill references cannot expand authority. The attack surface includes IDs, tenant arguments, embedded tool instructions, source manipulation and active output. All keys, accounts, orders and secrets are fixtures. A malicious machine administrator, real identity issuance, arbitrary document ingestion, hostile public networks and external side effects are outside the accepted scope. No web order-write endpoint exists. The older approved-write CLI is separately evaluated, not merged into the public UI.

## Implementation and evidence map

| Requirement | Implementation / fixed input | Actual evidence | Owner and remaining condition |
| --- | --- | --- | --- |
| Preserve original comparison | `baselines.py`; `ka0-v1.json`, `ka0-expected.json` | `capstone-run.json: lexical`, fresh 5/9, 6/9, 7/9 per language | Evaluation maintainer: do not change task denominator |
| Justify selection/format adaptation | `ka1.py`, `format_adaptation.py`; KA-1 contract/freeze and Chapter 38 adaptation files | Retained `ka1-run-v1.json`, `ka1-format-run-v1.json`, hashes in capstone run | Model owner: failed Mini GPT candidates remain rejected; no new training |
| Produce dated cited structure | `retrieval.py`, `rag.py`, `contracts.py`, `service_worker.py`; KA-2/4 fixtures | Fresh HTTP current 750, historical 600, boundary gate and abstention; exact schema/support checks | Policy owner: approve new intervals; synonym miss remains open |
| Use bounded workflow and reviewed Skill | Existing `workflow.py`, `source_skill.py`, reviewed source-verification package | Fresh worker Skill execution; retained bounded neural adapter evidence and fresh deterministic gate | Maintainer: extraction is default; no model-choice loop in the web path |
| Read-only Tool/MCP and host state | `mcp_readonly.py`, `read_tools.py`, `reliable_runtime.py`, `service.py` | Fresh subprocess exchange, 20 permission rows, HTTP tenant/owner rejection | Access administrator: fixtures are not production identity; KA-3/6 snapshots are distinct |
| Recover approved effects | `reliable_runtime.py`; exact approval/version/intent/receipt | Fresh after-commit lost response: `UNCERTAIN` to `DONE`, one final effect, zero replay writes | Reviewer/operator: manual compensation; no HTTP cancellation of orders |
| Layered evaluation and attacks | `system_eval.py`, `security_controls.py`; retained fixed cases | Fresh two 3/4 variants with different first failures; six guarded/unsafe comparisons | Evaluation/security maintainer: no pooled quality score or adaptive-attack estimate |
| Usable CPU service | `service.py`, `service_worker.py`, `service-ui/`; centralized bilingual content | Actual request/SSE/cancellation/error records; 12 CPU tests; service browser suite | UX maintainer: keyboard/labels/status reviewed; no full assistive-technology assessment |
| Trace, release and rollback | `service_ops.py`; independent release fixtures | A/B/stale 10/10, 10/10, 4/10; normal gate rejection; one-of-ten canary; 600 to 750 rollback, old in-flight 600 | Release owner: configuration-only local drill, no migration rollback |
| SLO, bounded failure and feedback | Cache, bucket, breaker, monitor and feedback classes | Fresh retry/deadline/overload/recovery; logical 18/20; injected window 2/5; reviewed boundary case | Operator/reviewer: bounded in-memory state; no production SLO inference |

Paths in this table are relative to `code/knowledge-assistant/` or `data/knowledge-assistant/` unless a Part IX record is named. Part IX results are in `data/part-ix/`. The four original bilingual diagrams are in `src/assets/ch-54/` through `ch-57/`; Chapter 57 links the normal request to independent boundary challenges rather than drawing a component inventory alone.

## Evaluation report

The frozen release task has five cases in two languages: current date, exact new-policy boundary, historical date, absent evidence and approval-policy reading. Independently authored expected status, amount and source precede the evaluator. A and B differ in response-cache TTL (30 versus 10 seconds) and both pass all ten presentations. The stale-date candidate forces 2025-09-14 and passes four; normal switching rejects it. These ten presentations are not a population benchmark, and the date-filtered task differs from the unchanged nine-query lexical baseline.

The lexical rerun reproduces Keyword 5/9, BoW Count 6/9 and TF-IDF 7/9 in each language. Keep those methods and old mistakes visible. The narrower service successfully answers the current and historical exact question but abstains on the supported-information paraphrase “overnight accommodation ceiling.” That known miss is not silently removed from the evidence. A future rewrite/index change must version its fixtures and protect date fidelity.

The two deliberately damaged layer variants each pass 3/4 while first failing at different boundaries. The six authored attack proposals all compromise the deliberately unsafe local fixtures and none compromises the guarded path. The 20-row permission matrix permits own north read, own south read and exactly approved cancellation; every other row is denied, with no unintended north effects. These samples establish named invariants against fixed conditions, not general security rates.

Historical model evidence is retained by hash. The rejected Mini GPT selection is unchanged. Earlier optional Qwen3 decision calls are not a new generator evaluation. The earlier judge's authored travel presentations match 8/8 but public human comparisons match 0/4; it is not accepted as the automatic graduation authority. No Part IX neural model call, training, external attack request or real business side effect occurs.

## Demonstrated operations and repaired defects

The actual local release journal includes canary, candidate switch, forced stale-date fault and return to A. New restored requests return 750; an old accepted stale request retains its snapshot and returns 600. Stored replay is identical with zero model calls and zero new effects. Read-only recomputation is a new request, not replay.

The fault window has five eligible jobs: a retry recovery, two failed jobs, an open rejection and a recovered probe. Two are good and three bad, so the measured injected window is 40%, with a demonstration burn ratio of 12 and an alert. The successful probe does not erase the failures. The separate authored 20-job calculation gives 18/20, a one-event 95% budget and burn 2; the strict greater-than-two alert is false. The records identify which times are measured and which clocks are assigned.

A cancellation initially emitted `dependency_failure` after `worker_stopped`. The retained initial trace and failing assertion exposed `InterruptedError` being caught as `OSError`; the exception order was corrected and the regression now forbids that event. The first service browser run had four failures caused by the store/UI `id` versus `order_id` mismatch. The service now explicitly projects the field; all six service UI checks passed in the subsequent run. Retained initial records prevent a clean final report from concealing these engineering failures.

## Deliverables and acceptance boundaries

- [Reproduction instructions](../code/part-ix/README.md), independently authored fixtures, exact dependencies and executed [Notebook 1](../notebooks/part-ix/01-service.ipynb) / [Notebook 2](../notebooks/part-ix/02-operations.ipynb).
- [Source research](part-ix-research.md), [dated fields/limits](part-ix-online.md), [run/rollback handbook](part-ix-runbook.md), and [validation with actual browser evidence](part-ix-validation.md).
- [Data/System Cards](../data/part-ix/cards-v1.json), [Risk Register](../data/part-ix/risk-register-v1.json), [license inventory](../data/part-ix/license-inventory-v1.json), and [record provenance](../data/part-ix/README.md).

The release checklist in the runbook maps each decision to evidence; it is not a fabricated external approval. Data and System Cards supplement, rather than overwrite, the earlier project cards. Risks retain explicit human owners. Original figures/data/prose use CC BY-SA 4.0, original code uses Apache-2.0, and inherited exceptions retain their own terms. No model weights or third-party figure is redistributed by Part IX.

Still unverified or unsupported: new neural-model quality, broad paraphrase retrieval, real-user identity and privacy operations, production load/capacity/availability, independent security audit, full WCAG conformance and assistive-technology user testing, Linux behavior and Windows process control, executable/database-migration rollback, remote MCP service interoperability, and long-duration retention under real use. None is silently claimed by passing local tests. Multimodal or multi-agent work is not an additional graduation prerequisite.
