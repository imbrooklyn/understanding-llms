# Part VII dated implementation layer

- `as_of: 2026-09-14`
- `last_verified: 2026-09-14`
- Local implementation: KA-2 context v1, answer schema `ka-answer-v1`, KA-3 order snapshot v1, KA-4 documents/eval v1.
- Protocol target: MCP **2026-07-28**. This is a tested synchronous stdio subset, not a claim of full SDK conformance.
- Actual CPU interpreter/dependencies: [run manifest](../data/part-vii/run-manifest.json), [tested dependency lock](../code/part-vii/requirements-tested.txt).

## Stable boundaries versus interface fields

The chapters explain selection, shape validation, execution authority, retrieval and support. This file records volatile protocol/provider fields separately. Core practice uses no external model or credential. The exact-source composer is replaceable through the `generator(context, documents, locale, on_date, topic)` callable in `rag.py`; a replacement must return the same answer contract and undergo the retained evaluation. A new callable is not evidence that a model passes KA-1 or KA-4.

## Official structured output example, not an executed experiment

The verified [Anthropic structured-output documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) uses `output_config.format` for raw JSON-schema output configuration and `strict: true` on strict tool definitions. A request fragment, with no selected model or actual call, is:

```json
{
  "output_config": {
    "format": {
      "type": "json_schema",
      "schema": {
        "type": "object",
        "properties": {"amount_yuan": {"type": ["integer", "null"]}},
        "required": ["amount_yuan"],
        "additionalProperties": false
      }
    }
  }
}
```

This fragment demonstrates the vendor envelope, not the full KA-2 contract. The application retains the complete Draft 2020-12 schema locally. The documented grammar subset does not enforce every numeric/string/array constraint. SDK transformations can remove unsupported constraints before sending and validate the original schema afterward. A field description is not an enforcement mechanism.

The current docs distinguish the raw request field from Python parsing convenience helpers and legacy beta compatibility. They also describe refusal and max-token stop reasons, and a string-enum capitalization caveat. Our local contract keeps exact enum matching and explicit failure branches rather than silently accepting differently cased states. Handle the provider envelope before parsing text. We did not install a vendor SDK, invoke constrained decoding, benchmark models, verify latency, or incur API charges. SDK/model availability must be rechecked when implementing an actual provider adapter.

## MCP current revision and tested surface

Primary references: [base fields](https://modelcontextprotocol.io/specification/2026-07-28/basic), [versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning), [stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio), [discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover), [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), and the official [TypeScript schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2026-07-28/schema.ts).

Every request includes `params._meta` with required `io.modelcontextprotocol/protocolVersion` and `io.modelcontextprotocol/clientCapabilities`; clientInfo is included for diagnostics. Each successful protocol result includes `resultType: complete` and serverInfo. Request IDs correlate replies; none authorizes an operation. Business identity is the fixture's trusted mira configuration, never self-reported clientInfo.

The client starts the server as a real child process and exchanges newline-delimited JSON-RPC messages. Discovery is optional for clients and implemented by this server. The server exposes only `get_order`. It does not expose Resources, Prompts, remote OAuth, subscriptions, MRTR, optional extensions or a write operation. Text and structured tool content represent the same server-produced value, unrelated to schema-constrained LLM output. Closing stdin terminates the child; the caller enforces a five-second process deadline.

The protocol rejects missing required metadata with -32602. Unsupported versions use -32022 with `data.supported` and `data.requested`, which differ from discovery's `supportedVersions`. Unknown methods use -32601; unknown tool names or invalid arguments use -32602. Forbidden ownership is a tool failure inside a complete result with `isError: true`. Tests cover those distinctions and correlation, not merely a happy-path mock function call.

## Compatibility and deprecation audit

The [latest specification](https://modelcontextprotocol.io/specification/latest) resolved to 2026-07-28 at verification time. Detailed per-request rules supersede leftover initialization wording in the high-level overview. This example does not send `initialize`/`initialized` or depend on a session header. Those belong to earlier revisions. The official compatibility matrix describes dual-era adapters; ours explicitly supports only the pinned revision and does not silently downgrade. An actual legacy deployment requires a separate tested path.

The [deprecation registry](https://modelcontextprotocol.io/specification/2026-07-28/deprecated), not a general migration slogan, controls dates:

| Feature | Status in the pinned revision | Boundary |
| --- | --- | --- |
| Roots, Sampling, Logging | Deprecated | New implementations should not adopt them; earliest removal is a revision on/after 2027-07-28 |
| Dynamic Client Registration | Deprecated | Migration path is Client ID Metadata Documents; same earliest-removal date |
| Older HTTP+SSE transport | Deprecated since an earlier revision | Registry specifies its separate SEP-2596 schedule; this is not removal of SSE from all transports |
| Tasks | Optional extension in the current architecture | Not a required feature of this read server |

Deprecated does not mean already removed. Stateless per-request interpretation does not prevent application state, changing order records or explicit operation handles. The HTTP authorization framework is not implemented by the local stdio fixture. A remote integration must separately implement transport requirements, credential handling and business access checks; changing the bind address is insufficient.

## Complete retained exchanges

The following is the actual subprocess demonstration record, rendered statically for review. It contains authored client requests and actual local server responses, including discovery, listing, a permitted read, a forbidden read and an unavailable cancellation. No model selected these calls.

```json
{
  "protocol_version": "2026-07-28",
  "transport": "actual subprocess stdio; no initialize handshake",
  "exchanges": [
    {
      "request": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "server/discover",
        "params": {
          "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
              "name": "book-host",
              "version": "1.0.0"
            }
          }
        }
      },
      "response": {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
          "resultType": "complete",
          "_meta": {
            "io.modelcontextprotocol/serverInfo": {
              "name": "book-orders",
              "version": "1.0.0"
            }
          },
          "supportedVersions": [
            "2026-07-28"
          ],
          "capabilities": {
            "tools": {}
          }
        }
      }
    },
    {
      "request": {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {
          "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
              "name": "book-host",
              "version": "1.0.0"
            }
          }
        }
      },
      "response": {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
          "resultType": "complete",
          "_meta": {
            "io.modelcontextprotocol/serverInfo": {
              "name": "book-orders",
              "version": "1.0.0"
            }
          },
          "tools": [
            {
              "name": "get_order",
              "description": "Read an owned fictional order snapshot; no mutation.",
              "inputSchema": {
                "type": "object",
                "properties": {
                  "order_id": {
                    "type": "string",
                    "pattern": "^A-[0-9]{3}$|^B-[0-9]{3}$"
                  }
                },
                "required": [
                  "order_id"
                ],
                "additionalProperties": false
              },
              "annotations": {
                "readOnlyHint": true,
                "destructiveHint": false,
                "idempotentHint": true,
                "openWorldHint": false
              }
            }
          ]
        }
      }
    },
    {
      "request": {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
          "name": "get_order",
          "arguments": {
            "order_id": "A-104"
          },
          "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
              "name": "book-host",
              "version": "1.0.0"
            }
          }
        }
      },
      "response": {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
          "resultType": "complete",
          "_meta": {
            "io.modelcontextprotocol/serverInfo": {
              "name": "book-orders",
              "version": "1.0.0"
            }
          },
          "content": [
            {
              "type": "text",
              "text": "{\"order_id\":\"A-104\",\"status\":\"processing\",\"as_of\":\"2026-09-14T00:00:00Z\",\"source_version\":\"ka3-orders-v1\"}"
            }
          ],
          "structuredContent": {
            "order_id": "A-104",
            "status": "processing",
            "as_of": "2026-09-14T00:00:00Z",
            "source_version": "ka3-orders-v1"
          },
          "isError": false
        }
      }
    },
    {
      "request": {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
          "name": "get_order",
          "arguments": {
            "order_id": "B-205"
          },
          "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
              "name": "book-host",
              "version": "1.0.0"
            }
          }
        }
      },
      "response": {
        "jsonrpc": "2.0",
        "id": 4,
        "result": {
          "resultType": "complete",
          "_meta": {
            "io.modelcontextprotocol/serverInfo": {
              "name": "book-orders",
              "version": "1.0.0"
            }
          },
          "content": [
            {
              "type": "text",
              "text": "{\"error\":\"forbidden\"}"
            }
          ],
          "structuredContent": {
            "error": "forbidden"
          },
          "isError": true
        }
      }
    },
    {
      "request": {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
          "name": "cancel_order",
          "arguments": {
            "order_id": "A-104"
          },
          "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
              "name": "book-host",
              "version": "1.0.0"
            }
          }
        }
      },
      "response": {
        "jsonrpc": "2.0",
        "id": 5,
        "error": {
          "code": -32602,
          "message": "Unknown tool"
        }
      }
    }
  ],
  "stderr": ""
}
```
