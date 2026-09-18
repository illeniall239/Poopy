# Curriculum Map

The fixed sequence of Topics the Tutor teaches. The Tutor adapts pacing, never content (ADR 0001). Changing this file is a deliberate, versioned decision.

**Budget:** about 976 h at 18 h/week ≈ 54 weeks. (481 h / 27 weeks until 2026-09-18, when five AI-foundations Phases (7–11, ~495 h) were added between full-stack and agents, and Phase 12 grew by four topics; the Learner chose depth over speed.) Phase hours include that Phase's share of daily Spaced Reviews (~15 min/Session) and, from Phase 3 on, the daily DSA Exercise (~20 min/Session, about 20 h per 4-week Phase). Interview Practice is a separate section and sits outside this budget.

**Tools change.** Framework Topics are taught against the current official docs when the Learner reaches that Phase. Versions named here were current on 2026-09-17.

**Exercises** exist in the app for Phases 1–2 (TypeScript, JavaScript, Python, Java) and Phases 7–11 (Python). Phases 3–6 and 12–13 are practised in the Learner's own projects and checked by Project Review.

**Audit.** On 2026-09-17 the Map was checked against the sources below (fetched pages, not memory): roadmap.sh TypeScript, JavaScript, Full Stack, Backend, Frontend, React, Node.js, System Design, AI Engineer and AI Agents topic lists (github.com/kamranahmedse/developer-roadmap, `roadmaps/<name>/content`); TypeScript Handbook; MDN JavaScript Guide; *Eloquent JavaScript* table of contents; NeetCode 150 categories (via a mirror — neetcode.io needs JavaScript); OWASP Top 10:2025; OWASP Top 10 for LLM Applications 2025; LangGraph v1 docs; Next.js docs (v16); react.dev. Gaps and ordering problems it found were fixed in this version.

| Phase | Hours | ≈ Weeks |
|---|---|---|
| 1. Problem solving and TypeScript fundamentals | 54 | 3.0 |
| 2. Data structures and algorithms | 71 | 3.9 |
| 3. Backend: Node, HTTP, APIs, Postgres | 77 | 4.3 |
| 4. Frontend: HTML, CSS, React, Next.js | 72 | 4.0 |
| 5. Security, testing, deployment — Portfolio Project 1 | 69 | 3.8 |
| 6. Real-time features and background jobs — Portfolio Project 2 | 42 | 2.3 |
| 7. Data and math for machine learning | 90 | 5.0 |
| 8. Classical machine learning | 105 | 5.8 |
| 9. Deep learning | 130 | 7.2 |
| 10. Transformers and large language models | 85 | 4.7 |
| 11. Vision, image generation, audio and multimodal models | 85 | 4.7 |
| 12. LLM apps and agents — Portfolio Project 3 | 80 | 4.4 |
| 13. System design basics and interview preparation | 34 | 1.9 |

**AI foundations (Phases 7–11), added 2026-09-18.** Researched against fetched syllabi and topic lists: Stanford CS229, CS231n, CS224n, CS236, CS234/CS285; MIT 6.S191; fast.ai parts 1–2; DeepLearning.AI ML and DL specialisations; Full Stack Deep Learning; Made With ML; Mathematics for Machine Learning; Dive into Deep Learning; Karpathy's Zero to Hero; 3Blue1Brown; Google's ML Crash Course, guides and glossary; Hugging Face LLM, Audio, Diffusion and MCP courses; roadmap.sh machine-learning, ai-data-scientist, mlops, ai-engineer and ai-agents; and the primary papers (Attention Is All You Need, ViT, CLIP, DDPM, Whisper, DPO). Full reports: `docs/research/`. Their must-have items that the old plan lacked (data work, project strategy, serving and monitoring, responsible AI, RL basics before RLHF) are in.

**"How it works" Topics.** Five big-picture Topics sit at the start of the Phase where they first matter: how computers run code (Phase 2), how the internet works and how databases work inside (Phase 3), how browsers work (Phase 4), how the cloud and deployment work (Phase 5). They are taught and reviewed like every other Topic. Their sources were added after the audit and are checked against the live pages when that Phase's Exercises are written.

**Deliberately left out** (judged not worth the hours for a first full-stack job): bit manipulation, math and geometry problems, Dijkstra, union-find, iterators/generators and regular expressions as Topics of their own, GraphQL, gRPC, Kafka, AWS in depth, Terraform, Ansible.

**Known tight spots:** Phases 5, 9 and 12 carry the most material for their hours. Where time runs short, the weekly check-in cuts the Topics marked *(light)* to a single Session first.

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

## Phase 7 — Data and math for machine learning (90 h)

Goal: the Learner can load, clean and explore a real dataset with NumPy, pandas and matplotlib, run an honest A/B test, and has every piece of linear algebra, calculus, probability and information theory that Phase 8 (classical ML) and Phase 9 (deep learning) consume, learned code-first and in the order those phases use it. Detail: [phase-7/PHASE.md](phase-7/PHASE.md).

1. NumPy arrays and vectorization
2. Vectors, dot product, norms
3. Matrices, matrix multiplication and broadcasting
4. Linear systems, inverse, determinant
5. pandas DataFrames and loading data
6. Visualization with matplotlib
7. EDA, data cleaning and data quality
8. Probability for ML
9. Inferential statistics and A/B testing
10. Derivatives and the chain rule
11. Partial derivatives, gradients and Jacobians
12. Optimization basics
13. Likelihood, entropy and cross-entropy
14. Eigenvectors and SVD, just enough for PCA


## Phase 8 — Classical machine learning (105 h)

Goal: the Learner can take a raw table to an honestly evaluated model: frame the task, beat a baseline, train linear, logistic, tree and ensemble models written from scratch, choose and tune them with cross-validation, cluster and reduce data, flag anomalies, recommend items, explain a tabular model, check it for unfairness, and say from an error analysis what to fix next. Detail: [phase-8/PHASE.md](phase-8/PHASE.md).

1. Framing a problem, baselines, and when not to use ML
2. Linear regression and MSE, closed form
3. Gradient descent for linear regression
4. Features: scaling, encoding and feature engineering
5. Train, validation, test, cross-validation and leakage
6. Overfitting, bias–variance and regularization
7. Logistic regression and binary cross-entropy
8. Classification metrics
9. Multiclass: softmax regression and categorical cross-entropy
10. k-nearest neighbors
11. Decision trees
12. Ensembles: bagging, random forests and gradient boosting
13. Interpretability for tabular models
14. Clustering: k-means
15. PCA and dimensionality reduction
16. Anomaly detection
17. Recommender systems basics
18. Responsible AI: fairness, bias and privacy
19. Error analysis and project strategy
20. The practical workflow: a scikit-learn-style capstone


## Phase 9 — Deep learning (130 h)

Goal: the Learner has built autograd from scratch, trains nets in PyTorch with their own loop, reads a training run like a mechanic, and is ready for attention and transformers in Phase 10. Detail: [phase-9/PHASE.md](phase-9/PHASE.md).

1. The neuron, MLPs and the forward pass
2. Activation functions
3. Computational graphs and backprop by hand
4. A scalar autograd engine (micrograd)
5. Loss functions for nets
6. Vectorized backprop: tensors and the backprop ninja
7. PyTorch fundamentals: tensors, autograd, nn.Module, the training loop
8. Optimizers and learning-rate schedules
9. Initialization and activation/gradient statistics
10. Normalization: BatchNorm and LayerNorm
11. Regularization in deep nets
12. Hyperparameter tuning methodology and experiment tracking
13. Convolutional networks
14. Modern CNN ideas: residual connections and transfer learning
15. Vision tasks beyond classification: detection and segmentation
16. GPUs, performance and debugging training
17. Embeddings
18. Sequence modeling: n-gram LM → MLP LM → RNN, LSTM, GRU
19. Capstone: a tiny CNN and a character-level LM from scratch


## Phase 10 — Transformers and large language models (85 h)

Goal: the Learner can build a GPT from tokenizer to sampler, and explain how it was pretrained, aligned and served, including why it hallucinates. Detail: [phase-10/PHASE.md](phase-10/PHASE.md).

1. Tokenization and BPE
2. Embeddings revisited: static, contextual and tied
3. Attention and self-attention from scratch
4. The transformer block
5. Encoder, decoder and encoder-decoder
6. The language-modelling objective and a tiny GPT
7. Scaling and pretraining
8. Fine-tuning, instruction tuning and LoRA
9. Reinforcement learning basics
10. RLHF and preference optimization (DPO)
11. Inference I: decoding and sampling
12. Inference II: KV cache, quantization and context windows
13. Hallucination, mechanically
14. Tokenization revisited and LLM quirks


## Phase 11 — Vision, image generation, audio and multimodal models (85 h)

Goal: the Learner can trace a prompt through Stable Diffusion, a waveform through Whisper, an image through a vision-language model, and say how each is evaluated. Detail: [phase-11/PHASE.md](phase-11/PHASE.md).

1. From CNNs to the Vision Transformer (ViT)
2. Contrastive learning and CLIP
3. Autoencoders, VAEs and VQ-VAE
4. GANs, briefly
5. Diffusion models: DDPM to DDIM
6. Latent diffusion and text-to-image conditioning
7. Evaluating image models
8. Audio as data
9. Speech recognition and Whisper
10. Audio tokens and neural codecs
11. Text-to-speech
12. Multimodal models
13. Evaluating generative models


## Phase 12 — LLM apps and agents — Portfolio Project 3 (80 h)

Goal: the Learner builds a reliable, observable LLM agent service in Python (LangGraph, FastAPI) and integrates it into a TypeScript full-stack app, with evals, tracing and guardrails they can defend. Python, uv, NumPy/pandas and PyTorch are assumed from Phases 7–11; how LLMs work inside (tokens, KV cache, quantization theory) from Phase 10. Detail: [phase-12/PHASE.md](phase-12/PHASE.md).

1. FastAPI for model and agent services
2. LLM API fundamentals: messages, tokens, streaming, structured output, prompt caching
3. Prompt and context engineering; evaluating outputs
4. Tool use (function calling)
5. Model Context Protocol (MCP): building a server, using one from a client
6. Retrieval-augmented generation: embeddings, chunking, vector search with pgvector
7. LangChain agents: `create_agent` and middleware
8. LangGraph: state, nodes, edges, checkpoints, memory, human-in-the-loop
9. Agent reliability: evals and tracing, guardrails, OWASP LLM Top 10 2025, cost and latency
10. Serving and deploying models: model as an API, batch vs online, latency and cost
11. Inference optimization and running local models
12. Monitoring, drift and observability for ML and LLM systems
13. Product and UX for AI features
14. Integrating an agent service into a TypeScript full-stack app
15. Portfolio Project 3: an AI agent app built with LangGraph


## Phase 13 — System design basics and interview preparation (34 h)

Goal: the Learner reasons through a junior-level system design question out loud, from requirements to a diagram with named trade-offs, including one that involves a model, and presents three portfolio projects and a work history convincingly. Detail: [phase-13/PHASE.md](phase-13/PHASE.md).

1. Requirements gathering and back-of-the-envelope estimation
2. Scaling stateless services: load balancers, horizontal scaling
3. Databases at scale: replication, read replicas, partitioning
4. Caching strategies and CDNs
5. Queues and asynchronous architectures
6. Consistency and availability trade-offs
7. Designing classic systems: URL shortener, rate limiter, chat, news feed
8. Designing ML and LLM systems
9. Behavioral interviews (STAR), resume, writing up portfolio projects, and ML/AI interview questions
