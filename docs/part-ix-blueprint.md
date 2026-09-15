# Part IX content blueprint

Status: authoring plan, 2026-09-14. Original documentation: CC BY-SA 4.0. This increment remains unpublished. The local service and release exercises never authorize website publication or external deployment.

## Audited starting point

The workspace contains separate book and main-site repositories. Existing uncommitted Part VII/VIII work is retained. The current publication state supersedes the older September 10 baseline: Chapters 1–39 and the Python Primer are published; Chapters 40–53 and the complete HTTP Primer are drafts. Chapters 54–57 contain placeholders. No applicable AGENTS.md was found. Existing heading numbering, KaTeX, bilingual static figures, local scrolling and production draft filtering are sufficient.

The eight accepted Part I bodies, their blueprint/research/validation/release records, public master plan sections 2–10, private corresponding plan, contribution guide, implementation plan and book configuration were audited. Prerequisite bodies include Chapters 31, 33, 38, 46–53 and both HTTP Primers. The shared KA implementation already contains immutable lexical comparisons, rejected Mini GPT candidates, structured contracts, date-filtered RAG, read-only tools/MCP, a bounded workflow, a source Skill, durable approval/recovery, layered evaluation and security controls. Historical validation is evidence of earlier runs, not a current pass.

No prerequisite is represented as a mere heading. A material scope boundary remains: neither Mini GPT candidate passed model selection; the accepted narrow answer path is deterministic extraction with source verification. Saved Qwen3-1.7B calls demonstrate a bounded decision adapter, not general answer quality. Part IX integrates the extractive path by default and preserves these negative selection results. Model/tokenizer fields explicitly record the absence of a neural generator in that mode. Optional model evidence remains separately attributed. The existing MCP teaching subset remains a separate local read-only transport; the service uses the tenant-aware order store and does not broaden its authority.

## Chapter 54: make a request usable

Question: why can a function returning 750 still leave a user unsure whether to wait, retry or trust the result? Baseline: a synchronous function with no request identity. Failure: cancellation hides the answer while work continues; a streamed unverified number looks final; another user's request ID leaks data.

Derive four responsibilities along one request: accessible UI, authenticated business control, dated retrieval, answer production/verification. Explain URL, JSON, accepted job versus completed result, event sequence and deadlines at the point of use, referring practice readers to the already complete HTTP Primer. The model layer is an adapter boundary; default extraction must not be described as measured model inference. Use actual loopback HTTP records for accepted/successful, unauthenticated, missing-evidence, cancelled and failed requests. A supplied timeline supports an independent queue/deadline calculation; measured durations are labeled separately.

Mechanisms: bounded concurrency, cooperative cancellation with a terminal-state lock, bounded safe-read retries, structured error responses, progress-event streaming, final-only validated citations. UX includes visible labels, keyboard focus, status messages, plain uncertainty, local handoff text and undo of displayed/draft state. It never suggests that undo reverses a committed order operation. Figure: request flow and cancellation race. Exercises: calculate remaining deadline, diagnose partial output, separate authentication/authorization, design a cancellation race assertion. KA-9: one integrated CPU service, actual request traces, layered tests, browser evidence. Handoff: which exact components produced a request?

## Chapter 55: make a release accountable

Question: why can the same named model answer differently after a policy/index change? Baseline: model name alone. Failure: a locally injected candidate changes the policy-date behavior and fails current-policy regression despite valid JSON. Record code, runtime, model/tokenizer applicability, prompt/context, immutable corpus, index recipe, schema, tools, Skill and UI hashes in a dependency graph. Explain a digest before relying on it.

Trace uses request identity, parent/child stage relationships, monotonic durations, outcome and manifest identity; sensitive content is separated from public diagnostics. Distinguish reading stored events, recomputing a read-only answer, calling a stochastic model again and recovering a side effect. Local release gates use independently authored outcomes and inherited baseline/attack evidence; candidates are evaluated on the same cases. A passing candidate can receive a predetermined small cohort; a deliberately forced bad local candidate demonstrates rollback to the retained good manifest. New requests switch; in-flight requests retain their snapshot. No deployment is performed.

Worked evidence: complete manifest row meanings, one failed candidate request, a gate conjunction, canary cohort arithmetic and actual switch/rollback journal. Figure: dependencies plus old/new/in-flight ownership. Exercises: missing tokenizer/context version, trace versus replay, a hard gate hidden by averages, and rollback with irreversible data. KA-10 increment: immutable candidate records, gate, local release checklist and rollback drill. Handoff: retained correctness still needs runtime resource bounds.

## Chapter 56: keep explicit service promises

Question: repeated questions save work, but what happens after policy updates or downstream failure? Baseline: question-only response cache. Counterexamples: historical/current date collision, tenant collision and semantic similarity across different amounts. Compare response/semantic caches with Chapter 31's prefix/KV state; semantic reuse stays disabled in the default service after a fixed false-match demonstration.

Define exact cache scope, release/data/date/language key, TTL boundary, authorization on every lookup, bounded storage and invalidation. Work through supplied time values with units. Derive a token-bucket calculation and a closed/open/half-open breaker timeline; verify implementations against independent expected states. Actual loopback faults demonstrate retry exhaustion, circuit-open fallback and successful recovery. Fallback is an explicit unavailable/handoff response, never stale policy stated as current.

Define eligible requests, good outcomes, latency limit, window endpoints, cancellation/rejection accounting, SLI, SLO and error budget from counted requests. Compute a small fixed window and burn ratio; actual smoke traffic is not a production availability estimate. Feedback pipeline accepts bounded categories, minimizes content, quarantines reports, requires an explicit maintainer review before a new regression enters a separate version, and supports expiry/deletion. Show selection bias using reporters and non-reporters. Figure: fault/recovery timeline and accounting. Exercises: TTL/date mismatch, refill arithmetic, SLO denominator, alert versus causal claim, feedback promotion. KA-10 increment: telemetry, alerts, controlled faults, reviewed regression. Handoff: collect these proofs against a requirement rather than a feature list.

## Chapter 57: graduate against evidence

Start with the fictional employee's dated-policy and own-order requirements, adversaries, assets, authority and human responsibilities. Follow a legitimate request, an unsupported synonym, a cross-tenant request, malicious data and a faulty release. Map each requirement to actual implementation, an independently specified expectation, current execution evidence and residual risk. Keep the same-set Keyword/Count/TF-IDF comparison and failed model/format-selection evidence; do not manufacture a single end-to-end score from incompatible test denominators.

Worked acceptance: decide which scope may be demonstrated locally and which claim must be withheld, using gates and unresolved failures. An architecture/evidence figure connects user value to evaluation and recovery. Deliver reproducible setup, retained baseline, selection rationale, layered regressions, evaluation report, license/dependency inventory, Risk Register, Data/System Cards, run/rollback handbooks and explicit human owners. The HTTP service has no order-write endpoint; the existing approved-write CLI remains a separately tested recovery exercise. No multimodal, multi-agent or industrial hosting prerequisite is introduced.

Exercises transfer the contract to a policy update, an approved cancellation with a lost response, a misleading benchmark aggregation and an unsupported external launch claim. Visible reference answers and a Part IX concept checkpoint complete the reading path. EXT-MM-01 remains untouched.

## Shared artifacts and research needs

Extend `code/knowledge-assistant/` with the service/runtime adapter and centralized UI resources. Use `code/part-ix/`, `data/part-ix/`, `notebooks/part-ix/` for bounded record runners, independently authored expectations and executed exercises. Retain earlier files and historical hashes. Public engineering text and implementation comments are English; textbook/UI localization lives in explicit content resources. Original data/figures/documentation use CC BY-SA 4.0; code uses Apache-2.0; inherited exceptions are listed individually.

Before technical drafting, verify Python's selected HTTP/threading stack, HTTP semantics and event framing, W3C accessibility guidance, OpenTelemetry trace semantics, Google's original SRE material, and NIST/OWASP governance/security material. Record actual supporting sections and limits in `part-ix-research.md`; version-sensitive commands belong in a dated online note. Do not infer present behavior from old screenshots.

## Verification and editorial acceptance

Use fixed small calculations independently of implementation; test observable HTTP behavior, ownership, terminal states, release snapshots, cache scope, retry bounds, breaker recovery, feedback review and unchanged inherited baselines. Execute notebooks from fresh kernels on the declared CPU environment. Add Part IX validation and browser coverage to repeatable project entries, then run the full existing CI build and browser suite against an owned local preview with BOOK_PREVIEW_URL set explicitly.

Review all eight pages at desktop/mobile sizes, light/dark diagrams, language switching and no-JavaScript evidence. Inspect actual generated screenshots. Verify production draft exclusion across routes, search, feeds, links and sitemap. First editorial pass checks claims, arithmetic and dependency contracts; second reads Chinese independently for causal flow before comparing bilingual facts, restrictions, references and answers. Record results only after execution in `part-ix-validation.md`.
