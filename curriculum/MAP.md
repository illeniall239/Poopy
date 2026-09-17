# Curriculum Map

The fixed sequence of Topics the Tutor teaches. The Tutor adapts pacing, never content (ADR 0001). Changing this file is a deliberate, versioned decision.

**Budget:** 481 h at 18 h/week ≈ 27 weeks. (26 weeks originally; about one week was added on 2026-09-17 for the five "how it works" Topics, so nothing job-critical got thinner.) Phase hours include that Phase's share of daily Spaced Reviews (~15 min/Session) and, from Phase 3 on, the daily DSA Exercise (~20 min/Session, about 20 h per 4-week Phase). Interview Practice is a separate section and sits outside this budget.

**Tools change.** Framework Topics are taught against the current official docs when the Learner reaches that Phase. Versions named here were current on 2026-09-17.

**Exercises** are written one Phase at a time, just before the Learner reaches it. Only Phase 1 has Exercises today.

**Audit.** On 2026-09-17 the Map was checked against the sources below (fetched pages, not memory): roadmap.sh TypeScript, JavaScript, Full Stack, Backend, Frontend, React, Node.js, System Design, AI Engineer and AI Agents topic lists (github.com/kamranahmedse/developer-roadmap, `roadmaps/<name>/content`); TypeScript Handbook; MDN JavaScript Guide; *Eloquent JavaScript* table of contents; NeetCode 150 categories (via a mirror — neetcode.io needs JavaScript); OWASP Top 10:2025; OWASP Top 10 for LLM Applications 2025; LangGraph v1 docs; Next.js docs (v16); react.dev. Gaps and ordering problems it found were fixed in this version.

| Phase | Hours | ≈ Weeks |
|---|---|---|
| 1. Problem solving and TypeScript fundamentals | 54 | 3.0 |
| 2. Data structures and algorithms | 71 | 3.9 |
| 3. Backend: Node, HTTP, APIs, Postgres | 77 | 4.3 |
| 4. Frontend: HTML, CSS, React, Next.js | 72 | 4.0 |
| 5. Security, testing, deployment — Portfolio Project 1 | 69 | 3.8 |
| 6. Real-time features and background jobs — Portfolio Project 2 | 42 | 2.3 |
| 7. Python, LLM apps, agents — Portfolio Project 3 | 66 | 3.7 |
| 8. System design basics and interview preparation | 30 | 1.7 |

**"How it works" Topics.** Five big-picture Topics sit at the start of the Phase where they first matter: how computers run code (Phase 2), how the internet works and how databases work inside (Phase 3), how browsers work (Phase 4), how the cloud and deployment work (Phase 5). They are taught and reviewed like every other Topic. Their sources were added after the audit and are checked against the live pages when that Phase's Exercises are written.

**Deliberately left out** (judged not worth the hours for a first full-stack job): bit manipulation, math and geometry problems, Dijkstra, union-find, iterators/generators and regular expressions as Topics of their own, GraphQL, gRPC, Kafka, AWS in depth, Terraform, Ansible.

**Known tight spots:** Phases 5 and 7 carry the most material for their hours. Where time runs short, the weekly check-in cuts the Topics marked *(light)* to a single Session first.

---

## Phase 1 — Problem solving and TypeScript fundamentals (54 h)

Goal: facing a blank problem, the Learner has a method, and can express the plan in TypeScript. Detail: [phase-1/PHASE.md](phase-1/PHASE.md).

1. A method for solving problems
2. Values, types, variables and expressions (including string basics and everyday type annotations)
3. Conditionals and boolean logic
4. Loops and tracing code by hand
5. Functions, breaking problems down, and scope
6. Arrays and accumulator patterns
7. Strings
8. Objects, Map and Set (including destructuring, spread and JSON)
9. TypeScript types: unions, narrowing, null safety, optional chaining
10. Higher-order functions and closures
11. Generics and utility types
12. Recursion
13. Errors and input validation (including `unknown` and type predicates)
14. Promises, async/await and the event loop
15. Reading and debugging code

Sources: TypeScript Handbook; MDN JavaScript Guide; *Eloquent JavaScript* (Haverbeke); *How to Solve It* (Pólya); *Think Like a Programmer* (Spraul); roadmap.sh TypeScript and JavaScript.

## Phase 2 — Data structures and algorithms (71 h)

Goal: the Learner picks a fitting data structure, states time and space complexity, and solves common interview patterns unaided. After the opening overview, order follows NeetCode's roadmap. After this Phase, one DSA Exercise runs in every Session.

1. How computers run code: CPU, memory, stack and heap, processes and threads, compiled vs interpreted, how a JavaScript engine runs your code
2. Big-O: time and space complexity
3. Classes for building data structures (including `this`)
4. Arrays and hashing
5. Two pointers
6. Sliding window
7. Stacks and queues
8. Binary search
9. Linked lists (including fast and slow pointers)
10. Sorting: merge sort, quicksort, and when built-in sort is enough
11. Trees: binary trees, BSTs, traversals
12. Tries
13. Heaps and priority queues
14. Backtracking
15. Graphs: representation, BFS, DFS, grid traversal
16. Dynamic programming: 1-D, then a few 2-D problems
17. Intervals and greedy algorithms

Sources: NeetCode 150 problem list and roadmap order (neetcode.io); roadmap.sh DSA topics; *Grokking Algorithms* (Bhargava); *The Algorithm Design Manual* (Skiena); *Code: The Hidden Language of Computer Hardware and Software* (Petzold); MDN "JavaScript execution model".

## Phase 3 — Backend: Node, HTTP, APIs, Postgres (77 h)

Goal: the Learner builds and explains a correct, well-structured REST API in TypeScript backed by Postgres.

1. How the internet works: packets, IP addresses, TCP and UDP, ports, DNS lookup step by step, what happens when you type a URL, the TLS handshake, hosting
2. Linux and terminal basics, git and GitHub workflow
3. npm, modules and a TypeScript project setup for Node
4. The Node runtime and its event loop in depth
5. HTTP: methods, status codes, headers, cookies, cache headers, CORS
6. REST API design: resources, errors, pagination, versioning, OpenAPI
7. Building the API with Express in TypeScript: routing, middleware, error handling (Hono and Fastify named as alternatives)
8. Validating input at trust boundaries (Zod)
9. Relational modeling: tables, keys, relationships, normalization
10. SQL: SELECT, JOIN, GROUP BY, subqueries
11. How databases work inside: pages on disk, B-tree indexes, the write-ahead log, MVCC
12. Indexes, reading query plans (EXPLAIN), and the N+1 query problem
13. Transactions and isolation levels *(conceptual)*
14. Using Postgres from Node: Drizzle, migrations, running Postgres locally with Docker Compose
15. Authentication fundamentals: password hashing, sessions and cookies vs tokens, CSRF
16. Logging and configuration
17. Practice Project: a REST API with Postgres

Sources: MDN "How the web works" and "What is a domain name?"; Cloudflare Learning Center (DNS, TLS); *Designing Data-Intensive Applications* (Kleppmann), chapter 3; PostgreSQL docs "Database Physical Storage" and "Write-Ahead Logging"; MDN HTTP docs; RFC 9110 (HTTP Semantics); Node.js docs; Express docs; OpenAPI Specification; PostgreSQL docs (tutorial, "Indexes", "Concurrency Control"); use-the-index-luke.com; Pro Git (git-scm.com/book); roadmap.sh Backend and Node.js.

## Phase 4 — Frontend: HTML, CSS, React, Next.js (72 h)

Goal: the Learner builds an accessible, responsive, fast frontend in Next.js that talks to a real API.

1. How browsers work: loading a page, parsing HTML and CSS, the DOM and CSSOM, layout and paint, where JavaScript runs
2. Semantic HTML and accessibility basics
3. CSS: box model, flexbox, grid, responsive layout
4. The DOM and events without a framework
5. React: components, props, state
6. React: effects, data fetching, forms, and what the React Compiler changes about memoization
7. Next.js App Router: routing, layouts, server and client components, Proxy
8. Next.js data: server actions, Cache Components, revalidation
9. Styling with Tailwind CSS
10. Client state and server state: TanStack Query, and when no state library is needed
11. Web performance basics: Core Web Vitals, Lighthouse *(light)*
12. Practice Project: a Next.js frontend for the Phase 3 API

Sources: MDN "Populating the page: how browsers work"; Chrome for Developers "Inside look at modern web browser"; MDN HTML, CSS and Accessibility docs; web.dev (Learn CSS, Learn Accessibility, Core Web Vitals); react.dev; nextjs.org/docs; TanStack Query docs; tailwindcss.com/docs; roadmap.sh Frontend and React.

## Phase 5 — Security, testing, deployment — Portfolio Project 1 (69 h)

Goal: the Learner ships a secure, tested, deployed full-stack app and can defend its security decisions.

1. OWASP Top 10:2025 applied: broken access control (including CSRF and SSRF), injection (including XSS), security misconfiguration and Content Security Policy, software supply chain (lockfiles, `npm audit`), mishandling exceptional conditions
2. Authentication and authorization done properly: OAuth/OIDC basics, role-based access, using an established auth library
3. Secrets and environment configuration
4. Unit and integration testing with Vitest, including against a real database
5. Component testing with React Testing Library
6. End-to-end testing with Playwright
7. CI with GitHub Actions
8. How the cloud and deployment work: physical servers, virtual machines, containers, serverless, PaaS, and everything between `git push` and a live URL
9. Docker: images, containers, Compose
10. Deploying a full-stack app with a managed Postgres
11. Observability: structured logs, metrics, error tracking
12. Portfolio Project 1: full-stack app with auth, Postgres, tests, CI, deployed

Sources: OWASP Top 10:2025 and OWASP Cheat Sheet Series; Vitest docs; Testing Library docs; Playwright docs; GitHub Actions docs; Docker docs; The Twelve-Factor App (12factor.net).

## Phase 6 — Real-time features and background jobs — Portfolio Project 2 (42 h)

Goal: the Learner adds work that happens outside the request/response cycle, safely.

1. WebSockets and Server-Sent Events
2. Pub/sub with Redis
3. Background job queues: retries, backoff, dead letters
4. Idempotency
5. Caching: Redis caching and invalidation (building on Phase 3 cache headers)
6. Rate limiting *(light)*
7. File uploads and object storage (S3-compatible) *(light)*
8. Portfolio Project 2: an app with real-time updates and background jobs

Sources: MDN WebSockets and Server-Sent Events docs; Redis docs; BullMQ docs; *Designing Data-Intensive Applications* (Kleppmann), chapters 11–12.

## Phase 7 — Python, LLM apps, agents — Portfolio Project 3 (66 h)

Goal: the Learner builds a reliable, observable LLM agent service and integrates it into a full-stack app.

1. Python for TypeScript developers: syntax, type hints, virtual environments and packaging with uv
2. FastAPI basics *(light)*
3. LLM API fundamentals: messages, tokens, streaming, structured output, prompt caching
4. Prompt and context engineering; evaluating outputs
5. Tool use (function calling)
6. Model Context Protocol (MCP): building a server, using one from a client
7. Retrieval-augmented generation: embeddings, chunking, vector search with pgvector
8. LangChain agents: `create_agent` and middleware
9. LangGraph: state, nodes, edges, checkpoints, memory, human-in-the-loop
10. Agent reliability: evals and tracing (LangSmith or Langfuse), guardrails, OWASP LLM Top 10 2025 (prompt injection, excessive agency, unbounded consumption), cost and latency
11. Integrating an agent service into a TypeScript full-stack app
12. Portfolio Project 3: an AI agent app built with LangGraph

Sources: docs.python.org tutorial; uv docs; FastAPI docs; Anthropic API docs (messages, tool use, prompt caching); modelcontextprotocol.io; LangChain v1 docs; LangGraph v1 docs; LangSmith / Langfuse docs; OWASP Top 10 for LLM Applications 2025; pgvector README; roadmap.sh AI Engineer and AI Agents.

## Phase 8 — System design basics and interview preparation (30 h)

Goal: the Learner can reason through a junior-level system design question out loud and present their portfolio convincingly.

1. Requirements gathering and back-of-the-envelope estimation
2. Scaling stateless services: load balancers, horizontal scaling
3. Databases at scale: replication, read replicas, partitioning
4. Caching strategies and CDNs
5. Queues and asynchronous architectures
6. Consistency and availability trade-offs
7. Designing classic systems: URL shortener, rate limiter, chat, news feed
8. Behavioral interviews (STAR), resume, and writing up portfolio projects

Sources: *Designing Data-Intensive Applications* (Kleppmann); *System Design Interview*, Vol. 1 (Alex Xu); roadmap.sh System Design.
