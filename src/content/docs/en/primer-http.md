---
title: "HTTP and API Foundations"
description: "Follow local HTTP requests, JSON responses, credentials, streaming and bounded failures."
published: 2026-09-15
sidebar:
  order: 102
---

## A program asks another program for an order

Before running Chapter 42's practice, complete this Primer. Reading its examples needs no account or programming experience. Running them uses the [Python Primer](/books/understanding-llms/en/primer-py/), Python 3.12 and the pinned environment in `code/part-vii/README.md`. Chapters 43 and 54 reuse these ideas.

A language model does not open an order database just by naming an order. Some program must send a request to a program that can read it. The requester is the **client**; the responder is the **server**. These are roles in an exchange, not necessarily two different computers. Our client and server both run locally, against fictional records.

An **API**, an application programming interface, is their agreed way to communicate: what requests are allowed and what results mean. **HTTP** supplies common request/response rules. JSON can carry data inside those messages. None of these requires a language model.

## Follow one request and response

**Example HTTP.1 — Read fictional A-104.** The scaffold binds to `127.0.0.1`, the loopback address of this computer, and asks the operating system for an unused port. For illustration only, suppose that port is 8765. The URL is `http://127.0.0.1:8765/orders/A-104`. `http` is the scheme, the address and port identify the receiving service, and `/orders/A-104` is the path within that service. A remote service might use an HTTPS hostname instead. HTTPS protects transport using TLS; it does not make the business response correct.

```http
GET /orders/A-104 HTTP/1.1
Host: 127.0.0.1:8765
Authorization: Bearer demo-placeholder-key

```

`GET` requests a representation. The first line also names the path and HTTP version. The following lines are **headers**, metadata such as which host receives the request and what credential the client presents. A blank line separates headers from a possible **body**. This request has no body. The displayed key is an intentionally public placeholder that works only with the local fixture.

```http
HTTP/1.0 200 OK
Content-Type: application/json

{"order_id":"A-104","status":"processing","as_of":"2026-09-14T00:00:00Z","source_version":"ka3-orders-v1"}
```

The scaffold's standard-library handler responds using HTTP/1.0; accepting an HTTP/1.1 request does not require echoing that version. This readable excerpt omits automatically generated Date, Server and Content-Length headers. The complete body is shown. `200` is a status code, and `Content-Type` tells the consumer how to interpret the body. Here the body is JSON: quoted field names, string values and commas inside braces. `status` is the order's state; 200 is the HTTP request's result. They answer different questions.

`as_of` is the snapshot time in UTC (`Z`). A successful response establishes what this fictional snapshot says, not an observation of a real order now. Repeating the same read may return a newer state in a real service without changing the meaning of “read.”

```book-figure
ch-42/http
```

Figure HTTP.1 locates the URL, credential, request outcome and business data. The client checks the response before using the order state. If the application later calls a model service, it becomes a client in a second exchange; the order server and model server remain different roles.

## A response can arrive successfully and still report failure

**Table HTTP.1 — Actual fixture routes and their meanings.**

| Request condition | Outcome | Client action |
| --- | --- | --- |
| GET own A-104 with placeholder credential | 200, processing snapshot | Validate body, use its timestamp |
| Missing/invalid credential | 401, unauthenticated | Correct authentication; do not blindly retry |
| GET another fictional owner's B-205 | 403, forbidden | Stop; a valid identity is not sufficient permission |
| GET nonexistent A-999 | 404, not_found | Report no available record |
| POST, attempting an unsupported write | 405, method_not_allowed | This scaffold only permits GET |
| GET `/rate-limit` | 429, rate_limited; Retry-After: 1 | Wait at least the indicated second if retry budget permits |
| Client waits 0.02 s for `/slow`, server delays 0.15 s | Client timeout | Server completion is unknown from this observation |

The first digit groups HTTP outcomes: 2xx generally indicates success, 4xx a request that cannot be fulfilled as sent, and 5xx a server-side failure. Individual codes still matter. A **timeout** is a local waiting limit, not another HTTP status code. The server may have completed work after the client stopped waiting.

A **retry** sends another request. For this read path we allow at most two attempts, a per-attempt timeout of 0.2 seconds, a total deadline of 1 second and backoff starting at 0.05 seconds. A 429 with Retry-After 1 consumes the remaining budget, so this policy stops instead of retrying early. A production service may require different settings; these are declared teaching choices, not performance recommendations. Rate limits are service policies, not something API keys bypass.

A read is usually safe to retry because it does not request a business mutation. HTTP calls such methods **safe**. **Idempotent** means repeating the same intended operation has the same intended effect as doing it once; it does not promise identical response text or no logging. A cancellation timeout is different: resending may repeat a side effect unless the service has a durable idempotency contract. Chapter 42 explains the static write case.

## Keep credentials out of notebooks and records

An API key is a credential the server checks, not model knowledge. For the optional local client exercise, an environment variable supplies it to the process:

```sh
export BOOK_DEMO_KEY=demo-placeholder-key
```

```python
import os
key = os.environ["BOOK_DEMO_KEY"]
```

The first command gives a named value to processes launched from that shell; the Python expression reads it. A missing variable raises `KeyError`, which should become a setup error rather than a request with an empty credential. Do not print the variable, put a real key in a URL, or save it in notebook output. Environment variables avoid hard-coding but are not a secret vault. Our saved traces replace credential values with `redacted`; our automatic demonstration uses only the fixed public placeholder.

Local and remote APIs share the request/response structure. They differ in trust, latency, authentication and transport protection. Binding this fixture to loopback avoids exposing it as a remote service. It is not a production authentication implementation and must not be repurposed by merely changing the bind address.

## Streaming changes when pieces arrive

Instead of waiting for one whole body, a server can send pieces while work proceeds. This is **streaming**. The fixture's `/stream` response uses `text/event-stream` and these three events:

```text
data: {"order_id": "A-104"}

data: {"status": "processing"}

data: {"complete": true}

```

A blank line terminates each event. A network read may stop halfway through `processing` or contain several events at once; network chunks are not event boundaries or model token boundaries. Buffer bytes, decode UTF-8 correctly and collect complete events. Under this fixture's application rule, only `complete: true` ends a usable result. A broken stream after the first event is incomplete, even if the HTTP status was 200. A streamed JSON answer may likewise need full assembly and validation before use.

## Run the local path and inspect its failures

From the book root, after creating the declared environment, run `python code/knowledge-assistant/http_scaffold.py`. It starts its own loopback server on an available port, performs the table's reads and streaming exchange, demonstrates the timeout, then closes the server. Its output contains no real credential. `data/part-vii/http-run.json` retains the actual execution record; it identifies itself as local HTTP, not model generation.

The Notebook shows `get(base, "/orders/A-104")`: `base` is the actual local address yielded by `server()`, not the illustrative 8765. The return values are HTTP status, parsed body and Retry-After. For streaming, the body remains text for event inspection. The program uses the same `lookup` function as the Tool and MCP adapter; there are not three independent order databases.

## Summary

The client sends a request to a server through an agreed API. HTTP supplies message semantics; JSON supplies a data representation. Credentials, status codes, timeouts and streaming completion each require their own interpretation. A successful read reports a source observation, while executing a write requires a separate authority and effect contract.

## Exercises

1. A response says HTTP 200 and JSON `"status":"processing"`. Which one tells you whether the order has shipped?
2. A read times out after 0.02 seconds. Can the client conclude that the server never looked up the order? What should the trace record?
3. The only streamed event received is the order ID. Can the client display “processing”? What information is missing?
4. Why should retrying a 401 differ from retrying a temporary 503? Under the fixture's 1-second total budget, should Retry-After 1 trigger an immediate retry?

## Reference answers

1. The body field concerns the order; 200 concerns the request. Here the snapshot says processing, not shipped. Check its timestamp before treating it as current.
2. No. Timeout establishes that the client did not receive a usable result within its limit. Record the attempt and unknown completion; do not label it as definitely unexecuted.
3. No. The status event and completion marker are missing. The order ID alone supplies no status, even if an earlier example used the same ID.
4. A 401 requires valid authentication, so repeating unchanged credentials will not repair it. A temporary 503 may permit bounded retry. Retry-After 1 is a waiting instruction; with less than one second remaining, stop instead of ignoring it.

## References

- [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), §§3–6, 9.2, 10.2.3, 11 and 15. Defines HTTP roles, messages, safe/idempotent semantics, authentication and statuses.
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html), §§2–8. Defines the JSON bodies and UTF-8 interchange.
- [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html), §4. Defines 429 and optional Retry-After without imposing one universal rate policy.
- [WHATWG Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html), §§9.2.4–9.2.6, verified 2026-09-14. Explains the event framing used by the local streaming fixture.
