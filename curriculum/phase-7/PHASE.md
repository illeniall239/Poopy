# Phase 7 — Python, LLM apps, agents — Portfolio Project 3

66 hours over about 4 weeks, 12 Topics. At the end the Learner builds a reliable, observable LLM agent service in Python (LangGraph, FastAPI) and integrates it into a TypeScript full-stack app, with evals, tracing and guardrails they can defend.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: Explain-back, later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during Explain-back and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-17.

---

## 1. Python for TypeScript developers

**Learned when:** the Learner translates a small TypeScript module (types, async functions, error handling, a class) into idiomatic typed Python in a uv-managed project and runs it with `uv run`.

**Teach:** indentation and blocks, `def`, `snake_case`; `list`/`dict`/`set`/`tuple` vs arrays, objects, Map, Set; comprehensions instead of `map`/`filter`; truthiness, `None`, `is`; f-strings; exceptions with `try`/`except`/`finally` and custom exception classes; type hints: `str | None`, `list[str]`, `TypedDict`, `dataclass`, `Protocol`, `Literal`, and a checker (pyright or mypy) as the `tsc` equivalent; `async def`/`await` and `asyncio` vs Node's event loop; modules and packages, `__init__.py`, relative imports; uv: `uv init`, `uv add`, `uv run`, `uv sync`, `uv lock`, `pyproject.toml`, `uv.lock` in git, `.venv` per project, `uv python` for versions; `ruff` for lint and format; `pytest` basics.

**Probe:** mutable default arguments; `==` vs `is` for `None`; thinking type hints are enforced at run time; `pip install` into the global interpreter; forgetting `await` returns a coroutine object silently; treating `dict` access like optional chaining.

**Practice:** Create a uv project and port the Phase 1 `parse-command` and `retry` exercises to typed Python with pytest tests and a pyright check. It works when `uv run pytest` and `uv run pyright` pass on a fresh clone with only `uv sync`, and the Learner can explain every line of `pyproject.toml`.

**Sources:** https://docs.astral.sh/uv/guides/projects/; https://docs.python.org/3/tutorial/index.html; https://docs.python.org/3/library/typing.html

## 2. FastAPI basics

**Learned when:** the Learner builds a small FastAPI service with typed request and response models, validation errors, a streaming endpoint and auto-generated OpenAPI docs, and maps each piece to its Express/Zod equivalent.

**Teach:** `app = FastAPI()`, path operation decorators `@app.get`/`@app.post`, path and query parameters typed in the signature; Pydantic models for bodies (the Zod of Python): validation, `model_dump`, 422 on failure; `response_model`; dependencies (`Depends`) for auth and shared resources; `async def` handlers and when a sync `def` is fine; `HTTPException`; `StreamingResponse` with `text/event-stream` for SSE; `fastapi dev main.py` for development, `fastapi run` or uvicorn in production; `/docs` and `/openapi.json` for free; settings from environment with `pydantic-settings`; CORS middleware; testing with `TestClient`.

**Probe:** doing blocking I/O inside `async def`; returning a dict where a model was promised; reading env vars all over instead of one settings object; skipping `response_model` and leaking fields; thinking `/docs` replaces writing a contract on purpose.

**Practice:** Build `agent-service` with `GET /health`, `POST /chat` (Pydantic body, echo response for now), an SSE endpoint that streams five numbered events, and a `Depends` that checks a shared secret header. It works when `/docs` shows the schemas, a bad body returns a 422 listing the field, and `curl -N` shows the events arriving one by one.

**Sources:** https://fastapi.tiangolo.com/tutorial/first-steps/; https://fastapi.tiangolo.com/tutorial/body/; https://fastapi.tiangolo.com/advanced/custom-response/

## 3. LLM API fundamentals: messages, tokens, streaming, structured output, prompt caching

**Learned when:** the Learner calls the Claude Messages API from Python with a system prompt and multi-turn messages, streams the reply to a terminal, gets validated JSON back with a schema, and shows a cache hit in the usage numbers.

**Teach:** the Messages API shape: `model`, `max_tokens`, `system`, `messages` with `role` and content blocks, `stop_reason`, `usage`; tokens: cost and context limits, `count_tokens` before sending, why long histories need trimming; temperature; streaming: `stream=True` gives server-sent events (`message_start`, `content_block_start`, `content_block_delta` with `text_delta`/`input_json_delta`, `message_delta`, `message_stop`), the SDK's `client.messages.stream()` helper; structured output: `output_config={"format": {"type": "json_schema", "schema": ...}}` for the response (the older `output_format` is replaced), and `strict: true` on tool definitions; prompt caching: `cache_control: {"type": "ephemeral"}` on the last stable block (or at the top level for automatic caching), minimum cacheable size per model, 5-minute default TTL or `ttl: "1h"`, reading `cache_creation_input_tokens` and `cache_read_input_tokens`; ordering: tools, system, then messages, with the changing part last; handling errors and rate limits with retries in the SDK; keys from the environment only.

**Probe:** putting the timestamp before the cache breakpoint and wondering why nothing caches; parsing JSON out of prose instead of asking for a schema; sending the whole history forever; treating the model's token count as characters; logging full prompts with user data; hard-coding the API key.

**Practice:** In `agent-service`, implement `/chat` for real: a cached system prompt, conversation history in memory keyed by a session id, streaming over SSE to the client, and a `/extract` endpoint that returns a Pydantic-validated object via `output_config`. It works when the second request's usage shows `cache_read_input_tokens > 0`, the stream arrives token by token in `curl -N`, and a malformed extraction is impossible by construction.

**Sources:** https://platform.claude.com/docs/en/api/messages; https://platform.claude.com/docs/en/build-with-claude/streaming; https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## 4. Prompt and context engineering; evaluating outputs

**Learned when:** the Learner improves a prompt by measurement, not taste: a small labeled dataset, a scoring function, a before/after number, and a written note of what changed and why.

**Teach:** the system prompt as a role, rules and output contract; be specific, give examples (few-shot), state the format; ordering: static instructions first, variable context, then the question; context engineering: what goes in the window (retrieved docs, tool results, summaries), what gets trimmed, and how to keep the stable prefix cacheable; asking for reasoning before answers when it helps; XML-style tags to separate sections; evaluation: build a dataset of 20–50 inputs with expected outputs or rubrics, score with exact match, code checks, or an LLM judge with a rubric, run it on every prompt change; separating "prompt bugs" from "model limits"; version prompts in git; cost and latency as metrics next to quality.

**Probe:** changing three things at once and eyeballing one example; a test set of the same five prompts the Learner wrote the prompt against; an LLM judge with no rubric; putting user input where instructions go (the injection seam, Topic 10); "it worked in the playground" as evidence.

**Practice:** For `/extract`, write a 30-case eval set (inputs plus expected fields), a pytest that scores field accuracy, and iterate the prompt three times recording the score each time in `evals/README.md`. It works when the score is reproducible run to run within noise and the final prompt beats the first measurably.

**Sources:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview; https://platform.claude.com/docs/en/build-with-claude/context-windows; https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

## 5. Tool use (function calling)

**Learned when:** the Learner writes the agent loop by hand: define tools with JSON Schema, run the model, execute `tool_use` blocks, return `tool_result` blocks, repeat until `stop_reason` is `end_turn`, with limits and error handling.

**Teach:** a tool is a name, a description the model reads, and an `input_schema`; the model never runs code, it asks: `stop_reason: "tool_use"` with `tool_use` blocks (`id`, `name`, `input`); the app runs the function and replies with a user message of `tool_result` blocks (`tool_use_id`, `content`, `is_error`); parallel tool calls and `tool_choice` (`auto`, `any`, a specific tool, `disable_parallel_tool_use`); `strict: true` for guaranteed schemas; the loop with an iteration cap, timeouts, and a token budget; tool descriptions as the main lever for good calls; tool results as untrusted input; keeping tool definitions before the cache breakpoint; the SDK's tool runner as the packaged version of the loop, after writing it by hand once.

**Probe:** letting the model "call" a tool by writing text; forgetting to send back the assistant's `tool_use` message before the `tool_result`; no cap on the loop; a tool that returns raw HTML pages of context; trusting a tool's output as instructions; tools with vague descriptions and then blaming the model.

**Practice:** Add two tools to `agent-service` (`search_items` over the Phase 3 API and `get_weather` or a calculator), implement the loop with a five-iteration cap and per-call timeouts, and log every tool call with arguments and duration. It works when a question needing two tools completes in one `/chat` call, a tool that throws produces an `is_error` result the model recovers from, and the loop stops at the cap with a clear message.

**Sources:** https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

## 6. Model Context Protocol (MCP): building a server, using one from a client

**Learned when:** the Learner builds an MCP server exposing two tools and a resource over stdio, tests it from an MCP host (Claude Desktop or Claude Code), then connects to it from their own client code, and explains what MCP standardizes that plain tool use did not.

**Teach:** the problem: every app re-implementing every integration; MCP roles: host (the LLM app), client (a connector inside it), server (the capability); JSON-RPC messages; per-request capability negotiation carried in `_meta` (the current spec, 2026-07-28, is stateless per request; earlier revisions used an `initialize` handshake); server features: tools (model calls), resources (data by URI), prompts (templates); client feature: elicitation (server asks the user for input); sampling and roots are deprecated in the current spec, so servers integrate with LLM APIs directly; transports: stdio for local subprocess servers, Streamable HTTP for remote ones; Python SDK: `from mcp.server import MCPServer`, `mcp = MCPServer("name")`, `@mcp.tool()` on typed functions with docstrings, `mcp.run(transport="stdio")`; TypeScript SDK: `McpServer` and `StdioServerTransport` from `@modelcontextprotocol/server`, `registerTool` with a Zod schema; wiring into a host via `mcpServers` config; tool descriptions are untrusted text from the host's point of view; the MCP connector in the Claude API for remote servers.

**Probe:** logging to stdout in a stdio server and corrupting the protocol; thinking MCP replaces the agent loop; building sampling or roots into a new server; exposing a "run any SQL" tool; confusing resources with tools; trusting a third-party server's tool descriptions.

**Practice:** Build `items-mcp` in Python exposing `search_items` and `get_item` tools plus an `items://recent` resource backed by the Phase 3 API, register it in Claude Desktop or Claude Code and use it in a conversation; then call it from `agent-service` with the MCP client SDK and route its tools into the Topic 5 loop. It works when the host lists the tools, a chat question triggers the tool with correct arguments, and the same server answers through the Learner's own client.

**Sources:** https://modelcontextprotocol.io/specification/latest; https://modelcontextprotocol.io/docs/develop/build-server; https://modelcontextprotocol.io/docs/develop/build-client

## 7. Retrieval-augmented generation: embeddings, chunking, vector search with pgvector

**Learned when:** the Learner builds a RAG pipeline end to end (chunk, embed, store in Postgres with pgvector, retrieve top-k, answer with citations) and measures retrieval quality on a small labeled set before tuning chunk size or k.

**Teach:** why RAG: knowledge the model lacks, freshness, citations, smaller prompts; embeddings as vectors where distance means similarity; Anthropic has no embedding model, so use a provider (Voyage AI is the documented option; any provider with the same `embed(texts)` shape works) with `input_type` query vs document; chunking: by structure (headings, paragraphs) with overlap, size in tokens, metadata (source, title, position); pgvector: `CREATE EXTENSION vector`, a `vector(1024)` column, cosine distance `<=>` (L2 `<->`, inner product `<#>`), an HNSW index for approximate search, filtering by metadata in the same query; hybrid search with Postgres full-text as a cheap boost; retrieval eval: for 20 questions, is the right chunk in the top k (recall@k); the answer prompt: retrieved chunks with ids, instruction to cite and to say "not found"; reranking as the next step; re-embedding when the model changes (version the column).

**Probe:** chunking by fixed character count through the middle of tables; comparing embeddings from different models; no index and calling it "fast enough" on 100 rows; k=20 chunks stuffed into the prompt; skipping retrieval eval and tuning the generation prompt instead; storing vectors with no reference to the source.

**Practice:** Ingest the Learner's own Phase 3–6 READMEs and decision logs into a `documents`/`chunks` schema with pgvector (Drizzle or SQL migrations), expose `/ask` in `agent-service` that retrieves top 5 and answers with chunk citations, and write a 20-question recall@5 eval. It works when recall@5 is measured before and after changing chunk size, `EXPLAIN` shows the HNSW index in use, and an off-topic question gets "not found in the documents".

**Sources:** https://github.com/pgvector/pgvector; https://platform.claude.com/docs/en/build-with-claude/embeddings

## 8. LangChain agents: `create_agent` and middleware

**Learned when:** the Learner rebuilds the Topic 5 loop with LangChain v1's `create_agent`, adds built-in and custom middleware, and explains what the framework does for them and what it hides.

**Teach:** `from langchain.agents import create_agent`; `create_agent(model="anthropic:claude-...", tools=[...], system_prompt=..., middleware=[...], response_format=PydanticModel, checkpointer=InMemorySaver())`; tools as plain typed functions or `@tool`; `agent.invoke({"messages": [...]}, config={"configurable": {"thread_id": ...}})` and streaming; the agent as "model + harness": the harness is middleware around each model and tool call; built-in middleware: `SummarizationMiddleware` (trim long histories), `HumanInTheLoopMiddleware` (approve tool calls), `ModelCallLimitMiddleware` and tool-call limits, `ToolRetryMiddleware`, `ModelFallbackMiddleware`, PII detection; custom middleware via decorators `@before_agent`, `@before_model`, `@after_model`, `@after_agent`, `@wrap_model_call`, `@wrap_tool_call`, `@dynamic_prompt`, or an `AgentMiddleware` subclass; where limits, logging and guardrails belong (middleware, not the prompt); the same graph underneath is LangGraph (Topic 9).

**Probe:** stuffing rate limits and safety rules into the system prompt; thinking `create_agent` removes the need to understand the loop; a `thread_id` shared by all users; letting an agent run with no call limit; middleware that mutates state without returning it.

**Practice:** Replace the hand-written loop in `agent-service` with `create_agent` using the same two tools, add `ModelCallLimitMiddleware`, `SummarizationMiddleware`, a custom `@wrap_tool_call` that logs and times every tool, and a `@dynamic_prompt` that injects the current user's name. It works when the Topic 4 eval set scores the same or better, a runaway prompt stops at the call limit, and a 40-turn conversation stays under the token budget thanks to summarization.

**Sources:** https://docs.langchain.com/oss/python/langchain/agents; https://docs.langchain.com/oss/python/langchain/middleware; https://docs.langchain.com/oss/python/langchain/middleware/custom

## 9. LangGraph: state, nodes, edges, checkpoints, memory, human-in-the-loop

**Learned when:** the Learner designs a multi-step workflow as an explicit graph (typed state, nodes, conditional edges), persists it with a Postgres checkpointer so it survives restarts, and pauses it for human approval with `interrupt`.

**Teach:** when a fixed loop is not enough: branching, retries with different strategies, parallel steps, approvals; `StateGraph` with a `TypedDict` state and reducers (`Annotated[list, add_messages]`); nodes as functions returning partial state; `add_edge`, `add_conditional_edges` with a routing function, `START`/`END`; `graph.compile(checkpointer=...)`: `InMemorySaver` for dev, `PostgresSaver` for real; `thread_id` in `config` as the conversation/run key, state history and time travel; short-term memory (the thread) vs long-term memory (`Store`, keyed by user, searchable); human-in-the-loop: `interrupt(payload)` inside a node stops the run, the client resumes with `Command(resume=value)`; `Command` for routing plus state update from a node; streaming node outputs and tokens; visualizing the graph; testing nodes in isolation.

**Probe:** putting everything in one node; state as a bare dict with no reducer so messages get overwritten; forgetting the checkpointer and losing the interrupt; a `thread_id` that is not unique per user and conversation; resuming an interrupt by re-invoking with new input instead of `Command(resume=...)`; treating long-term memory as a place to dump every message.

**Practice:** Build a "request refund" (or similar) workflow in `agent-service`: classify → gather details with tools → if amount above a threshold, `interrupt` for approval → execute → summarize, with `PostgresSaver` on the project's Postgres and a `/runs/{thread_id}/resume` endpoint. It works when restarting the service mid-interrupt and then resuming completes the run, the state history shows every step, and the graph diagram in the README matches the code.

**Sources:** https://docs.langchain.com/oss/python/langgraph/graph-api; https://docs.langchain.com/oss/python/langgraph/persistence; https://docs.langchain.com/oss/python/langgraph/interrupts

## 10. Agent reliability: evals and tracing, guardrails, OWASP LLM Top 10 2025, cost and latency

**Learned when:** the Learner can show, for the agent, a trace of one run, an eval run with a score history, a guardrail that stops a prompt-injection attempt, and a per-request cost and latency number, and explains which OWASP LLM risks each control addresses.

**Teach:** tracing: LangSmith (`LANGSMITH_TRACING=true` plus API key traces LangChain/LangGraph automatically) or Langfuse (`CallbackHandler` in `config["callbacks"]`, `@observe`, self-hostable, OpenTelemetry-based); what a trace shows: every model call, tool call, tokens, latency, errors; evals as CI: datasets, evaluators (code, LLM-as-judge with a rubric), `evaluate()` in LangSmith or Langfuse datasets, regression on every prompt or graph change; OWASP Top 10 for LLM Applications 2025: LLM01 Prompt Injection (direct and indirect via tool results and retrieved documents), LLM06 Excessive Agency (least-privilege tools, approval for destructive actions), LLM10 Unbounded Consumption (limits on calls, tokens, time, cost per user), plus LLM02 Sensitive Information Disclosure and LLM05 Improper Output Handling (never render or execute model output unescaped); guardrails: input classification, tool allow-lists per user, output validation with schemas, `HumanInTheLoopMiddleware` for risky tools, rate limits from Phase 6; cost and latency: tokens per request, cache hit rate, p95, model choice per step (small model for routing, larger for answers), streaming for perceived latency; alerting on failure rate and cost.

**Probe:** "the system prompt says to ignore injections" as the defense; a tool that can delete anything exposed to every user; no per-user cost ceiling; treating a passing eval on 10 cases as proof; tracing off in production "for privacy" with no alternative; measuring average latency and not p95.

**Practice:** Turn on tracing for `agent-service`, add a red-team eval set of 15 injection and abuse prompts (including one hidden in a retrieved document and one in a tool result), implement a per-user token and call budget plus a tool allow-list, and record cost and p95 per endpoint on a dashboard. It works when every red-team case is blocked or safely refused, the eval runs in CI on every change, and one trace link explains a failed run end to end.

**Sources:** https://genai.owasp.org/llm-top-10/; https://docs.langchain.com/langsmith/observability-quickstart; https://langfuse.com/docs/observability/get-started

## 11. Integrating an agent service into a TypeScript full-stack app

**Learned when:** the Learner connects the Next.js/Express app to `agent-service` so a user can chat with the agent in the browser with streamed tokens, approvals and history, with the Python service never exposed directly to the public.

**Teach:** the shape: browser → Next.js (session, authorization, rate limit) → agent-service over a private network with a service secret → model and tools; passing the user's identity and permissions to the agent (never the session cookie); streaming end to end: FastAPI SSE → Route Handler or Server Function that re-streams → `EventSource` or `fetch` with a `ReadableStream` in a Client Component; conversation threads stored by `thread_id` per user; the approval UI for `interrupt`: show the pending action, resume via the API; timeouts and cancellation (`AbortController` → client disconnect → cancel the run); error states and retries; cost attribution per user; running both services in Compose and deploying them side by side; contract tests against the FastAPI OpenAPI schema with a generated TypeScript client.

**Probe:** calling the Python service from the browser with the API key in the bundle; letting the agent trust a `user_id` field the browser sent; buffering the whole reply and then sending it; no timeout so a hung run holds a connection forever; a chat that forgets history on refresh; skipping authorization "because the agent only reads".

**Practice:** Add `/assistant` to the Portfolio Project 1 app: a chat Client Component with streamed tokens, thread history from `agent-service`, and an approval card for interrupted runs; the Python service is reachable only from the app's network. It works when tokens appear as they are generated, a refund over the threshold shows an approval card that resumes the run, closing the tab cancels the run in the traces, and a direct request to the Python service from the internet is refused.

**Sources:** https://fastapi.tiangolo.com/advanced/custom-response/; https://nextjs.org/docs/app/getting-started/mutating-data; https://docs.langchain.com/oss/python/langgraph/interrupts

## 12. Portfolio Project 3: an AI agent app built with LangGraph

**Learned when:** the Learner ships a deployed AI agent product (Next.js front, TypeScript API, Python LangGraph service, Postgres with pgvector, tracing, evals in CI) with a README that explains the graph, the guardrails and the numbers, and can defend it in a technical interview.

**Teach:** picking a domain where an agent with tools and retrieval beats a plain chat (support over the Learner's own data, an operations assistant, a research helper); the graph drawn before code; tools with least privilege; RAG over real documents; human approval on any destructive step; eval set with a score history and a red-team set; cost and latency budget per request with alerts; tracing in production with personal data handled; the README: architecture diagram, graph diagram, guardrails, eval results table, cost per conversation, failure modes and what the user sees; a demo account and a recorded walkthrough; reusing Projects 1 and 2 (auth, CI, Docker, queues) rather than rebuilding.

**Probe:** a wrapper around one prompt called an "agent"; no evals or a single screenshot as evidence; unlimited tools and no approval step; secrets in the Python service's image; a README that can't answer "how much does a conversation cost".

**Practice:** Build, deploy and document the project over the final week and a half, then run the fresh-clone test (Compose brings up all services), the eval suite, and the red-team set on the deployed app. It works when the evals pass in CI, the traces show every run, the guardrails hold against the red-team set, and the Tutor's mock interview on the architecture finds no decision the Learner cannot justify.

**Sources:** https://docs.langchain.com/oss/python/langgraph/overview; https://genai.owasp.org/llm-top-10/; https://docs.langchain.com/langsmith/evaluation
