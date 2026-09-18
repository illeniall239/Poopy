# Phase 12 — LLM apps and agents — Portfolio Project 3

80 hours over about 4½ weeks, 15 Topics. At the end the Learner builds a reliable, observable LLM agent service in Python (LangGraph, FastAPI) and integrates it into a TypeScript full-stack app, with evals, tracing and guardrails they can defend. Python, uv, NumPy/pandas and PyTorch are assumed from Phases 7–11; how LLMs work inside (tokens, KV cache, quantization theory) from Phase 10.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: Explain-back, later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during Explain-back and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-18.

---

## 1. FastAPI for model and agent services

**Learned when:** the Learner builds a small FastAPI service with typed request and response models, a streaming endpoint and a `lifespan` that loads a model once, and maps each piece to its Express/Zod equivalent.

**Teach:** `app = FastAPI()`, `@app.get`/`@app.post`, path and query parameters typed in the signature; Pydantic models for bodies (the Zod of Python): validation, 422 on failure, `response_model`; `Depends` for auth and shared resources; `async def` handlers vs sync `def` for blocking work (model inference is blocking: FastAPI runs sync `def` in a threadpool); `HTTPException`; `StreamingResponse` with `text/event-stream` for SSE; `lifespan` with `@asynccontextmanager`: load the model before `yield`, release after, never at import time; `fastapi dev` vs `fastapi run`/uvicorn; `/docs` and `/openapi.json` for free; `pydantic-settings` for configuration; CORS middleware; `TestClient`.

**Probe:** doing blocking inference inside `async def` and stalling every request; loading the model inside the handler on every call; returning a dict where a model was promised; reading env vars all over instead of one settings object; thinking `/docs` replaces writing a contract on purpose.

**Practice:** Build `agent-service` in the Phase 7 uv setup with `GET /health`, `POST /chat` (Pydantic body, echo for now), an SSE endpoint that streams five numbered events, a `Depends` that checks a shared secret header, and a `lifespan` that loads the Phase 8 classifier once. It works when `/docs` shows the schemas, a bad body returns a 422 listing the field, `curl -N` shows the events arriving one by one, and the model loads exactly once in the logs.

**Sources:** https://fastapi.tiangolo.com/tutorial/first-steps/; https://fastapi.tiangolo.com/tutorial/body/; https://fastapi.tiangolo.com/advanced/events/; https://fastapi.tiangolo.com/advanced/custom-response/

## 2. LLM API fundamentals: messages, tokens, streaming, structured output, prompt caching

**Learned when:** the Learner calls the Claude Messages API from Python with a system prompt and multi-turn messages, streams the reply to a terminal, gets validated JSON back with a schema, and shows a cache hit in the usage numbers.

**Teach:** the Messages API shape: `model`, `max_tokens`, `system`, `messages` with `role` and content blocks, `stop_reason`, `usage`; tokens: cost and context limits, `count_tokens` before sending, why long histories need trimming; temperature; streaming: `stream=True` gives server-sent events (`message_start`, `content_block_start`, `content_block_delta` with `text_delta`/`input_json_delta`, `message_delta`, `message_stop`), the SDK's `client.messages.stream()` helper; structured output: `output_config={"format": {"type": "json_schema", "schema": ...}}` for the response (the older `output_format` is replaced), and `strict: true` on tool definitions; prompt caching: `cache_control: {"type": "ephemeral"}` on the last stable block (or at the top level for automatic caching), minimum cacheable size per model, 5-minute default TTL or `ttl: "1h"`, reading `cache_creation_input_tokens` and `cache_read_input_tokens`; ordering: tools, system, then messages, with the changing part last; handling errors and rate limits with retries in the SDK; keys from the environment only.

**Probe:** putting the timestamp before the cache breakpoint and wondering why nothing caches; parsing JSON out of prose instead of asking for a schema; sending the whole history forever; treating the model's token count as characters; logging full prompts with user data; hard-coding the API key.

**Practice:** In `agent-service`, implement `/chat` for real: a cached system prompt, conversation history in memory keyed by a session id, streaming over SSE to the client, and a `/extract` endpoint that returns a Pydantic-validated object via `output_config`. It works when the second request's usage shows `cache_read_input_tokens > 0`, the stream arrives token by token in `curl -N`, and a malformed extraction is impossible by construction.

**Sources:** https://platform.claude.com/docs/en/api/messages; https://platform.claude.com/docs/en/build-with-claude/streaming; https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## 3. Prompt and context engineering; evaluating outputs

**Learned when:** the Learner improves a prompt by measurement, not taste: a small labeled dataset, a scoring function, a before/after number, and a written note of what changed and why.

**Teach:** the system prompt as a role, rules and output contract; be specific, give examples (few-shot), state the format; ordering: static instructions first, variable context, then the question; context engineering: what goes in the window (retrieved docs, tool results, summaries), what gets trimmed, and how to keep the stable prefix cacheable; asking for reasoning before answers when it helps; XML-style tags to separate sections; evaluation: build a dataset of 20–50 inputs with expected outputs or rubrics, score with exact match, code checks, or an LLM judge with a rubric, run it on every prompt change; separating "prompt bugs" from "model limits"; version prompts in git; cost and latency as metrics next to quality.

**Probe:** changing three things at once and eyeballing one example; a test set of the same five prompts the Learner wrote the prompt against; an LLM judge with no rubric; putting user input where instructions go (the injection seam, Topic 9); "it worked in the playground" as evidence.

**Practice:** For `/extract`, write a 30-case eval set (inputs plus expected fields), a pytest that scores field accuracy, and iterate the prompt three times recording the score each time in `evals/README.md`. It works when the score is reproducible run to run within noise and the final prompt beats the first measurably.

**Sources:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview; https://platform.claude.com/docs/en/build-with-claude/context-windows; https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

## 4. Tool use (function calling)

**Learned when:** the Learner writes the agent loop by hand: define tools with JSON Schema, run the model, execute `tool_use` blocks, return `tool_result` blocks, repeat until `stop_reason` is `end_turn`, with limits and error handling.

**Teach:** a tool is a name, a description the model reads, and an `input_schema`; the model never runs code, it asks: `stop_reason: "tool_use"` with `tool_use` blocks (`id`, `name`, `input`); the app runs the function and replies with a user message of `tool_result` blocks (`tool_use_id`, `content`, `is_error`); parallel tool calls and `tool_choice` (`auto`, `any`, a specific tool, `disable_parallel_tool_use`); `strict: true` for guaranteed schemas; the loop with an iteration cap, timeouts, and a token budget; tool descriptions as the main lever for good calls; tool results as untrusted input; keeping tool definitions before the cache breakpoint; the SDK's tool runner as the packaged version of the loop, after writing it by hand once.

**Probe:** letting the model "call" a tool by writing text; forgetting to send back the assistant's `tool_use` message before the `tool_result`; no cap on the loop; a tool that returns raw HTML pages of context; trusting a tool's output as instructions; tools with vague descriptions and then blaming the model.

**Practice:** Add two tools to `agent-service` (`search_items` over the Phase 3 API and `get_weather` or a calculator), implement the loop with a five-iteration cap and per-call timeouts, and log every tool call with arguments and duration. It works when a question needing two tools completes in one `/chat` call, a tool that throws produces an `is_error` result the model recovers from, and the loop stops at the cap with a clear message.

**Sources:** https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

## 5. Model Context Protocol (MCP): building a server, using one from a client

**Learned when:** the Learner builds an MCP server exposing two tools and a resource over stdio, tests it from an MCP host (Claude Desktop or Claude Code), then connects to it from their own client code, and explains what MCP standardizes that plain tool use did not.

**Teach:** the problem: every app re-implementing every integration; MCP roles: host (the LLM app), client (a connector inside it), server (the capability); JSON-RPC messages; per-request capability negotiation carried in `_meta` (the current spec, 2026-07-28, is stateless per request; earlier revisions used an `initialize` handshake); server features: tools (model calls), resources (data by URI), prompts (templates); client feature: elicitation (server asks the user for input); sampling and roots are deprecated in the current spec, so servers integrate with LLM APIs directly; transports: stdio for local subprocess servers, Streamable HTTP for remote ones; Python SDK: `from mcp.server import MCPServer`, `mcp = MCPServer("name")`, `@mcp.tool()` on typed functions with docstrings, `mcp.run(transport="stdio")`; TypeScript SDK: `McpServer` and `StdioServerTransport` from `@modelcontextprotocol/server`, `registerTool` with a Zod schema; wiring into a host via `mcpServers` config; tool descriptions are untrusted text from the host's point of view; the MCP connector in the Claude API for remote servers.

**Probe:** logging to stdout in a stdio server and corrupting the protocol; thinking MCP replaces the agent loop; building sampling or roots into a new server; exposing a "run any SQL" tool; confusing resources with tools; trusting a third-party server's tool descriptions.

**Practice:** Build `items-mcp` in Python exposing `search_items` and `get_item` tools plus an `items://recent` resource backed by the Phase 3 API, register it in Claude Desktop or Claude Code and use it in a conversation; then call it from `agent-service` with the MCP client SDK and route its tools into the Topic 4 loop. It works when the host lists the tools, a chat question triggers the tool with correct arguments, and the same server answers through the Learner's own client.

**Sources:** https://modelcontextprotocol.io/specification/latest; https://modelcontextprotocol.io/docs/develop/build-server; https://modelcontextprotocol.io/docs/develop/build-client

## 6. Retrieval-augmented generation: embeddings, chunking, vector search with pgvector

**Learned when:** the Learner builds a RAG pipeline end to end (chunk, embed, store in Postgres with pgvector, retrieve top-k, answer with citations) and measures retrieval quality on a small labeled set before tuning chunk size or k.

**Teach:** why RAG: knowledge the model lacks, freshness, citations, smaller prompts; embeddings as vectors where distance means similarity (Phase 10 built them; here they are a service call); Anthropic has no embedding model, so use a provider (Voyage AI is the documented option; any provider with the same `embed(texts)` shape works, including a local model from Topic 11) with `input_type` query vs document; chunking: by structure (headings, paragraphs) with overlap, size in tokens, metadata (source, title, position); pgvector: `CREATE EXTENSION vector`, a `vector(1024)` column, cosine distance `<=>` (L2 `<->`, inner product `<#>`), an HNSW index for approximate search, filtering by metadata in the same query; hybrid search with Postgres full-text as a cheap boost; retrieval eval: for 20 questions, is the right chunk in the top k (recall@k); the answer prompt: retrieved chunks with ids, instruction to cite and to say "not found"; reranking as the next step; re-embedding when the model changes (version the column).

**Probe:** chunking by fixed character count through the middle of tables; comparing embeddings from different models; no index and calling it "fast enough" on 100 rows; k=20 chunks stuffed into the prompt; skipping retrieval eval and tuning the generation prompt instead; storing vectors with no reference to the source.

**Practice:** Ingest the Learner's own Phase 3–6 READMEs and decision logs into a `documents`/`chunks` schema with pgvector (Drizzle or SQL migrations), expose `/ask` in `agent-service` that retrieves top 5 and answers with chunk citations, and write a 20-question recall@5 eval. It works when recall@5 is measured before and after changing chunk size, `EXPLAIN` shows the HNSW index in use, and an off-topic question gets "not found in the documents".

**Sources:** https://github.com/pgvector/pgvector; https://platform.claude.com/docs/en/build-with-claude/embeddings

## 7. LangChain agents: `create_agent` and middleware

**Learned when:** the Learner rebuilds the Topic 4 loop with LangChain v1's `create_agent`, adds built-in and custom middleware, and explains what the framework does for them and what it hides.

**Teach:** `from langchain.agents import create_agent`; `create_agent(model="anthropic:claude-...", tools=[...], system_prompt=..., middleware=[...], response_format=PydanticModel, checkpointer=InMemorySaver())`; tools as plain typed functions or `@tool`; `agent.invoke({"messages": [...]}, config={"configurable": {"thread_id": ...}})` and streaming; the agent as "model + harness": the harness is middleware around each model and tool call; built-in middleware: `SummarizationMiddleware` (trim long histories), `HumanInTheLoopMiddleware` (approve tool calls), `ModelCallLimitMiddleware` and tool-call limits, `ToolRetryMiddleware`, `ModelFallbackMiddleware`, PII detection; custom middleware via decorators `@before_agent`, `@before_model`, `@after_model`, `@after_agent`, `@wrap_model_call`, `@wrap_tool_call`, `@dynamic_prompt`, or an `AgentMiddleware` subclass; where limits, logging and guardrails belong (middleware, not the prompt); the same graph underneath is LangGraph (Topic 8).

**Probe:** stuffing rate limits and safety rules into the system prompt; thinking `create_agent` removes the need to understand the loop; a `thread_id` shared by all users; letting an agent run with no call limit; middleware that mutates state without returning it.

**Practice:** Replace the hand-written loop in `agent-service` with `create_agent` using the same two tools, add `ModelCallLimitMiddleware`, `SummarizationMiddleware`, a custom `@wrap_tool_call` that logs and times every tool, and a `@dynamic_prompt` that injects the current user's name. It works when the Topic 3 eval set scores the same or better, a runaway prompt stops at the call limit, and a 40-turn conversation stays under the token budget thanks to summarization.

**Sources:** https://docs.langchain.com/oss/python/langchain/agents; https://docs.langchain.com/oss/python/langchain/middleware; https://docs.langchain.com/oss/python/langchain/middleware/custom

## 8. LangGraph: state, nodes, edges, checkpoints, memory, human-in-the-loop

**Learned when:** the Learner designs a multi-step workflow as an explicit graph (typed state, nodes, conditional edges), persists it with a Postgres checkpointer so it survives restarts, and pauses it for human approval with `interrupt`.

**Teach:** when a fixed loop is not enough: branching, retries with different strategies, parallel steps, approvals; `StateGraph` with a `TypedDict` state and reducers (`Annotated[list, add_messages]`); nodes as functions returning partial state; `add_edge`, `add_conditional_edges` with a routing function, `START`/`END`; `graph.compile(checkpointer=...)`: `InMemorySaver` for dev, `PostgresSaver` for real; `thread_id` in `config` as the conversation/run key, state history and time travel; short-term memory (the thread) vs long-term memory (`Store`, keyed by user, searchable); human-in-the-loop: `interrupt(payload)` inside a node stops the run, the client resumes with `Command(resume=value)`; `Command` for routing plus state update from a node; streaming node outputs and tokens; visualizing the graph; testing nodes in isolation.

**Probe:** putting everything in one node; state as a bare dict with no reducer so messages get overwritten; forgetting the checkpointer and losing the interrupt; a `thread_id` that is not unique per user and conversation; resuming an interrupt by re-invoking with new input instead of `Command(resume=...)`; treating long-term memory as a place to dump every message.

**Practice:** Build a "request refund" (or similar) workflow in `agent-service`: classify → gather details with tools → if amount above a threshold, `interrupt` for approval → execute → summarize, with `PostgresSaver` on the project's Postgres and a `/runs/{thread_id}/resume` endpoint. It works when restarting the service mid-interrupt and then resuming completes the run, the state history shows every step, and the graph diagram in the README matches the code.

**Sources:** https://docs.langchain.com/oss/python/langgraph/graph-api; https://docs.langchain.com/oss/python/langgraph/persistence; https://docs.langchain.com/oss/python/langgraph/interrupts

## 9. Agent reliability: evals and tracing, guardrails, OWASP LLM Top 10 2025, cost and latency

**Learned when:** the Learner can show, for the agent, a trace of one run, an eval run with a score history, a guardrail that stops a prompt-injection attempt, and a per-request cost and latency number, and explains which OWASP LLM risks each control addresses.

**Teach:** tracing: LangSmith (`LANGSMITH_TRACING=true` plus API key traces LangChain/LangGraph automatically, `@traceable` for plain functions) or Langfuse (OpenTelemetry-based, self-hostable, `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`/`LANGFUSE_BASE_URL`, `@observe` or `start_as_current_observation`); what a trace shows: every model call, tool call, tokens, latency, errors; evals as CI: datasets, evaluators (code, LLM-as-judge with a rubric), `evaluate()` in LangSmith or Langfuse datasets, regression on every prompt or graph change; OWASP Top 10 for LLM Applications 2025: LLM01 Prompt Injection (direct and indirect via tool results and retrieved documents), LLM06 Excessive Agency (least-privilege tools, approval for destructive actions), LLM10 Unbounded Consumption (limits on calls, tokens, time, cost per user), plus LLM02 Sensitive Information Disclosure and LLM05 Improper Output Handling (never render or execute model output unescaped); guardrails: input classification, tool allow-lists per user, output validation with schemas, `HumanInTheLoopMiddleware` for risky tools, rate limits from Phase 6; cost and latency: tokens per request, cache hit rate, p95, model choice per step (small model for routing, larger for answers), streaming for perceived latency; alerting on failure rate and cost.

**Probe:** "the system prompt says to ignore injections" as the defense; a tool that can delete anything exposed to every user; no per-user cost ceiling; treating a passing eval on 10 cases as proof; tracing off in production "for privacy" with no alternative; measuring average latency and not p95.

**Practice:** Turn on tracing for `agent-service`, add a red-team eval set of 15 injection and abuse prompts (including one hidden in a retrieved document and one in a tool result), implement a per-user token and call budget plus a tool allow-list, and record cost and p95 per endpoint on a dashboard. It works when every red-team case is blocked or safely refused, the eval runs in CI on every change, and one trace link explains a failed run end to end.

**Sources:** https://genai.owasp.org/llm-top-10/; https://docs.langchain.com/langsmith/observability-quickstart; https://langfuse.com/docs/observability/get-started

## 10. Serving and deploying models: model as an API, batch vs online, latency and cost

**Learned when:** the Learner puts one of their own Phase 8–11 models behind an HTTP endpoint in a container, chooses batch or online inference for a given feature with the reason written down, and reports p95 latency, throughput and cost per 1,000 predictions for it.

**Teach:** the four shapes: model-in-service (inside the web app), model-as-a-service (its own API, the usual sweet spot), batch prediction (run on a schedule, store the results), edge/on-device (Topic 11); static (offline) inference: cheap, verifiable before release, but only for inputs you predicted and stale by hours; dynamic (online) inference: any input, long tail, but compute-heavy, latency-sensitive and harder to monitor; the same split for LLM work: the Claude Message Batches API (`client.messages.batches.create` with `custom_id` per request, results within 24 hours, half price) for evals, backfills and nightly jobs vs the Messages API for chat; serving a model: `lifespan` loads weights once, a sync `def` handler or a worker process so inference never blocks the event loop, a fixed `/predict` contract with a version field, warm-up on start, a health check that actually runs the model; batching requests on the server to use the GPU (or CPU) well; CPU is enough for most small models, GPU only when measured; containers: pin weights by hash, keep them out of the image layer or in it deliberately, size the memory; scaling horizontally with the Phase 13 load-balancer picture; what to measure: p50/p95 latency, requests per second, cost per 1,000 predictions, error rate; a Gradio or Streamlit prototype in a day before any of this.

**Probe:** hosting on a GPU because training used one; loading the model per request; a health check that returns 200 while the model failed to load; batch predictions with no timestamp so nobody knows they are stale; choosing online inference for a nightly report; average latency instead of p95; "it's fast on my laptop" as a capacity plan.

**Practice:** Wrap the Phase 8 or Phase 11 model as `model-service` (FastAPI, Docker, `/predict`, `/health`, model version in every response), load-test it with a small script at 10 and 100 concurrent requests recording p95 and errors, then move one feature of the portfolio app to a nightly batch job whose results land in Postgres, and run the Topic 3 eval set through the Batches API. It works when the README states p95, throughput and cost per 1,000 for the online path and the batch job's cost and freshness, and the Learner can say which features belong on which path and why.

**Sources:** https://fullstackdeeplearning.com/course/2022/lecture-5-deployment/; https://developers.google.com/machine-learning/crash-course/production-ml-systems/static-vs-dynamic-inference; https://fastapi.tiangolo.com/advanced/events/; https://platform.claude.com/docs/en/build-with-claude/batch-processing; https://madewithml.com/courses/mlops/serving/

## 11. Inference optimization and running local models

**Learned when:** the Learner runs an open-weights LLM locally with Ollama and a small model in the browser with Transformers.js, points the existing agent code at each with no other change, and can say from measurements when a quantized local model is the right call and when it is not.

**Teach:** what Phase 10 taught made practical: quantization (fp16 → int8 → int4, GGUF files) trades a little quality for memory and speed, the KV cache sets the context ceiling, prefill is compute-bound and decode is memory-bandwidth-bound; Ollama: `ollama pull`/`run`/`list`/`ps`, `ollama serve` on `localhost:11434`, model tags pick size and quantization, `/api/chat` (`model`, `messages`, `tools`, `format` as `"json"` or a JSON schema, `options`, `stream`, `keep_alive`) and the OpenAI-compatible `/v1/chat/completions` and `/v1/embeddings` so existing SDKs work with a `base_url` swap and any `api_key`; timings in the response (`prompt_eval_count`, `eval_count`, `eval_duration` in nanoseconds) to compute tokens per second; importing a GGUF with a `Modelfile` `FROM /path/to/file.gguf` (quantize first with llama.cpp's `llama-quantize`, Ollama does not); vLLM for serving open models at scale: `vllm serve <model>` gives an OpenAI-compatible server on port 8000, continuous batching for throughput, `quantization=` for AWQ/GPTQ/FP8/GGUF weights, `LLM(...).generate()` for offline batch; Transformers.js: `pipeline(task, model, { device: 'webgpu', dtype: 'q4' })` from `@huggingface/transformers` runs ONNX models in the browser (WASM on CPU by default, `q8` default there), so embeddings, Whisper or a classifier can run with no server and no data leaving the device, in a Web Worker so the UI stays responsive; the decision: privacy, offline, cost per token at volume, and latency on the one hand; quality ceiling, hardware, operations burden and eval results on the other; server-side batching and caching before buying GPUs.

**Probe:** treating a 4-bit 7B model as interchangeable with a frontier model without running the eval set; measuring tokens per second once and calling it capacity; running the browser model on the main thread; forgetting that a "free" local model costs the user's battery and download; picking a context length the KV cache cannot hold; assuming quantization always makes compute faster (it mostly saves memory and bandwidth); shipping a local model with no fallback when WebGPU is missing.

**Practice:** Run `agent-service` against Ollama by changing only the client base URL and model name, run the Topic 3 and Topic 6 eval sets against the local model and the API model, recording score, tokens per second and cost; then add a Transformers.js embedding or classification feature to the portfolio app in a Web Worker with a server fallback. It works when the README shows the local-vs-API comparison table with numbers and a one-paragraph decision, the browser feature works offline in DevTools, and the fallback triggers in a browser without WebGPU.

**Sources:** https://docs.ollama.com/api/chat; https://docs.ollama.com/openai; https://docs.ollama.com/quickstart; https://docs.ollama.com/import; https://docs.vllm.ai/en/latest/getting_started/quickstart/; https://docs.vllm.ai/en/latest/features/quantization/; https://huggingface.co/docs/transformers.js/index; https://huggingface.co/docs/transformers.js/guides/webgpu

## 12. Monitoring, drift and observability for ML and LLM systems

**Learned when:** the Learner instruments a deployed model and the agent so that a silent quality drop shows up on a dashboard within a day, with a drift report, a quality score per trace, and an alert that names what to check.

**Teach:** models decay silently: performance is only guaranteed on data like the training data; what to monitor: input data quality (schema, ranges, counts, nulls), input distribution drift (sudden from a bug, gradual from users changing, seasonal, temporary from an attack), prediction distribution, delayed ground truth and proxy metrics when labels arrive late, real-world outcomes and user feedback, performance by slice ("a successful whole sometimes obscures an unsuccessful subset"), training-serving skew (schema skew and feature skew), model age since retrain, feedback loops where predictions feed the next training set; the loop: log everything with context → detect → curate data → retrain → offline test → deploy, which is why logging is the first monitoring feature; Evidently: `Dataset.from_pandas(df, data_definition=DataDefinition(...))`, `Report([DataDriftPreset()]).run(current, reference)`, `.json()`/`.save_html()`, run on a schedule against a reference window; for LLMs the same ideas through traces: Langfuse scores (`create_score(name, value, trace_id, data_type)`, `score_current_trace`) from user thumbs, LLM-judge sampling and code checks, cost and token usage per trace, latency percentiles, error and refusal rate, tool-failure rate, retrieval hit rate; dashboards and alerts wired into the Phase 5 observability stack; an observability mindset: keep raw inputs and outputs (with personal data handled) so unknown failures can be debugged after the fact; deciding the retrain or re-prompt trigger up front.

**Probe:** monitoring only uptime and p95 and calling the model "monitored"; averaging over all users and missing one broken segment; waiting for labels that never come instead of a proxy; a drift alert with no threshold anyone agreed on; a feedback loop the model trains on its own outputs; logging nothing "for privacy" instead of redacting; thumbs-up rate as the only quality signal.

**Practice:** Add a nightly Evidently drift report for `model-service` comparing the last day's inputs to a reference sample (alert in the Phase 5 stack when drift is flagged), and for `agent-service` log a Langfuse score per trace from user feedback plus a sampled LLM-judge score, with a dashboard of quality, cost, latency and tool-failure rate by day. It works when injecting shifted inputs trips the drift alert the next run, a deliberately broken prompt drops the judge score within a day on the dashboard, and each alert says which page to open next.

**Sources:** https://fullstackdeeplearning.com/course/2022/lecture-6-continual-learning/; https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring; https://docs.evidentlyai.com/quickstart_ml; https://langfuse.com/docs/evaluation/evaluation-methods/custom-scores

## 13. Product and UX for AI features

**Learned when:** the Learner decides for a proposed feature whether it needs a model at all, and if so designs the interaction (expectation-setting, confidence, feedback, human-in-the-loop, failure states) and writes the success metric before building it.

**Teach:** Rules of ML: don't be afraid to launch without ML, design the metrics first, choose ML over a complex heuristic once you have data, keep the first model simple and get the infrastructure right; the model is a small part of a large system; the People + AI Guidebook chapters as a checklist: User Needs + Defining Success (augment or automate, what "good" means, precision vs recall in product terms), Data Collection + Evaluation, Mental Models (explain benefits not technology, state limits, onboard in stages), Explainability + Trust (show sources, confidence, and what the system cannot do), Feedback + Control (cheap feedback that actually improves the system, user override), Errors + Graceful Failure (fallbacks when the model is wrong, uncertain or down); human-in-the-loop as a design choice: approve, edit, or escalate, and where the `interrupt` from Topic 8 shows up in the UI; confidence thresholds and "I don't know"; latency budgets and streaming as UX; the cost of a false positive vs a false negative for this feature; disclosure that the user is talking to a model; a success metric that is a user outcome, not model accuracy; the feature's failure UX drawn before the happy path.

**Probe:** adding a chatbot because everyone has one; measuring accuracy and never the user's outcome; a feature with no state for "the model was wrong"; anthropomorphic copy that hides that it is a model; a thumbs-down button that goes nowhere; asking users to correct the model without showing what it got wrong; a spinner for 20 seconds where streaming or a batch job fits.

**Practice:** For three proposed features in the portfolio apps, write a one-page brief each: is ML needed (and the heuristic if not), the user outcome metric, the interaction sketch with confidence, feedback and failure states, human-in-the-loop points, and the latency budget; then implement the failure UX and feedback capture for the one that ships, wired to Topic 12's scores. It works when a Tutor role-playing a sceptical PM cannot find a state the design leaves the user stuck in, one feature was talked out of ML on purpose, and the shipped feature's feedback appears in the quality dashboard.

**Sources:** https://developers.google.com/machine-learning/guides/rules-of-ml; https://pair.withgoogle.com/guidebook-v2/chapters/mental-models/; https://developers.google.com/machine-learning/crash-course/production-ml-systems; https://fullstackdeeplearning.com/course/2022/lecture-5-deployment/

## 14. Integrating an agent service into a TypeScript full-stack app

**Learned when:** the Learner connects the Next.js/Express app to `agent-service` so a user can chat with the agent in the browser with streamed tokens, approvals and history, with the Python service never exposed directly to the public.

**Teach:** the shape: browser → Next.js (session, authorization, rate limit) → agent-service over a private network with a service secret → model and tools; passing the user's identity and permissions to the agent (never the session cookie); streaming end to end: FastAPI SSE → Route Handler or Server Function that re-streams → `EventSource` or `fetch` with a `ReadableStream` in a Client Component; conversation threads stored by `thread_id` per user; the approval UI for `interrupt`: show the pending action, resume via the API; timeouts and cancellation (`AbortController` → client disconnect → cancel the run); error states and retries (the Topic 13 failure UX); cost attribution per user; running `agent-service` and `model-service` in Compose and deploying them side by side; contract tests against the FastAPI OpenAPI schema with a generated TypeScript client.

**Probe:** calling the Python service from the browser with the API key in the bundle; letting the agent trust a `user_id` field the browser sent; buffering the whole reply and then sending it; no timeout so a hung run holds a connection forever; a chat that forgets history on refresh; skipping authorization "because the agent only reads".

**Practice:** Add `/assistant` to the Portfolio Project 1 app: a chat Client Component with streamed tokens, thread history from `agent-service`, and an approval card for interrupted runs; the Python services are reachable only from the app's network. It works when tokens appear as they are generated, a refund over the threshold shows an approval card that resumes the run, closing the tab cancels the run in the traces, and a direct request to the Python service from the internet is refused.

**Sources:** https://fastapi.tiangolo.com/advanced/custom-response/; https://nextjs.org/docs/app/getting-started/mutating-data; https://docs.langchain.com/oss/python/langgraph/interrupts

## 15. Portfolio Project 3: an AI agent app built with LangGraph

**Learned when:** the Learner ships a deployed AI agent product (Next.js front, TypeScript API, Python LangGraph service, Postgres with pgvector, tracing, evals in CI, monitoring) with a README that explains the graph, the guardrails, the serving choices and the numbers, and can defend it in a technical interview.

**Teach:** picking a domain where an agent with tools and retrieval beats a plain chat (support over the Learner's own data, an operations assistant, a research helper), with the Topic 13 brief written first; the graph drawn before code; tools with least privilege; RAG over real documents; human approval on any destructive step; eval set with a score history and a red-team set; cost and latency budget per request with alerts; tracing and quality scores in production with personal data handled; one batch path and one online path, and one local or browser model if the numbers justified it; the README: architecture diagram, graph diagram, guardrails, eval results table, cost per conversation, serving decisions with measurements, failure modes and what the user sees; a demo account and a recorded walkthrough; reusing Projects 1 and 2 (auth, CI, Docker, queues) rather than rebuilding.

**Probe:** a wrapper around one prompt called an "agent"; no evals or a single screenshot as evidence; unlimited tools and no approval step; secrets in the Python service's image; a README that can't answer "how much does a conversation cost" or "how would you know if it got worse".

**Practice:** Build, deploy and document the project over the final week and a half, then run the fresh-clone test (Compose brings up all services), the eval suite, and the red-team set on the deployed app. It works when the evals pass in CI, the traces show every run, the dashboard shows quality and cost by day, the guardrails hold against the red-team set, and the Tutor's mock interview on the architecture finds no decision the Learner cannot justify.

**Sources:** https://docs.langchain.com/oss/python/langgraph/overview; https://genai.owasp.org/llm-top-10/; https://docs.langchain.com/langsmith/evaluation
