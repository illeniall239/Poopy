# Phase 3 — Backend: Node, HTTP, APIs, Postgres

77 hours over about 4 weeks, 17 Topics. At the end the Learner builds and explains a correct, well-structured REST API in TypeScript backed by Postgres, and can defend every layer of it from the socket up.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: a passed Project Review, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-17.

---

## 1. How the internet works

**Learned when:** the Learner narrates what happens between typing a URL and seeing a page, naming each hop (DNS, TCP, TLS, HTTP) and what would break if that hop failed.

**Teach:** packets and why data is chopped up; IP addresses (v4 and v6) and routing hop by hop; TCP (ordered, reliable, handshake) vs UDP (fire and forget); ports as "which program on this machine"; DNS lookup step by step: stub resolver, cache, recursive resolver, root, TLD, authoritative, TTL; the full URL-to-page story; the TLS handshake: certificate, key exchange, then symmetric encryption, and what a CA vouches for; hosting: a server is a machine with a public IP and a process listening on a port.

**Probe:** thinking HTTPS hides the domain name from the network (SNI); believing DNS is one lookup to one server; UDP treated as "broken TCP" rather than a trade-off; assuming localhost:3000 is reachable from another machine; thinking a domain and a server are the same thing.

**Practice:** In a terminal, trace a real request by hand: `nslookup` or `dig` for a domain, then `curl -v https://example.com` and label every line of output (resolution, connect, TLS, request, response headers). It works when the Learner can point to the TLS and HTTP parts of the output and explain the certificate line.

**Sources:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works; https://www.cloudflare.com/learning/dns/what-is-dns/; https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/

## 2. Linux and terminal basics, git and GitHub workflow

**Learned when:** the Learner works a task entirely from the terminal (navigate, inspect, edit, run) and ships it as a branch, commit and pull request without touching a GUI.

**Teach:** the filesystem tree, paths, permissions; `ls`, `cd`, `cat`, `grep`, `find`, pipes and redirection; environment variables and `PATH`; processes, `ps`, `kill`, ports in use; git's model: working tree, index, commits as snapshots, branches as pointers; `status`/`diff`/`add`/`commit`/`log`; branching and merging; `rebase` vs `merge`; resolving conflicts; `.gitignore`; remotes, `fetch`/`pull`/`push`; the GitHub flow: branch, PR, review, merge; writing a useful commit message and PR description.

**Probe:** thinking `git add` saves to the repo; believing a branch is a copy of the files; fearing `git pull` will delete local work; committing `node_modules` or `.env`; treating "force push" as a normal fix; not knowing where a detached HEAD came from.

**Practice:** In the Learner's project, create a feature branch, make two commits, deliberately create a merge conflict with `main`, resolve it, and open a PR on GitHub with a description that explains the why. It works when `git log --oneline --graph` shows the expected history and the PR merges cleanly.

**Sources:** https://git-scm.com/book/en/v2; https://docs.github.com/en/get-started/using-github/github-flow

## 3. npm, modules and a TypeScript project setup for Node

**Learned when:** the Learner sets up a Node + TypeScript project from an empty folder, explains every line of `package.json` and `tsconfig.json`, and runs, type-checks and builds it.

**Teach:** `package.json`: `dependencies` vs `devDependencies`, `scripts`, `"type": "module"`; `package-lock.json` and `npm ci`; semver ranges; ES modules vs CommonJS and why Node needs to know which; `import`/`export`, `node:` built-ins; `tsconfig.json`: `strict`, `target`, `module`, `outDir`, `noEmit`; two ways to run TypeScript: Node's built-in type stripping (`node file.ts` on Node 22.18+/24, erasable syntax only, no type checking) vs compiling with `tsc`; `tsc --noEmit` as the type check; `.env` files and `process.env`; picking an LTS Node version.

**Probe:** thinking `npm install` makes the lockfile irrelevant; believing Node type-checks when it runs a `.ts` file; using `require` in an ESM project and vice versa; committing built output; treating `^` ranges as "exactly this version".

**Practice:** From an empty directory, create the API project the rest of this Phase builds on: `npm init`, TypeScript with `strict: true`, a `dev` script that runs a `.ts` entry with Node directly, a `check` script running `tsc --noEmit`, and a `build` script. It works when a deliberate type error fails `npm run check` but a clean file runs with `npm run dev`.

**Sources:** https://nodejs.org/en/learn/typescript/run-natively; https://nodejs.org/api/packages.html; https://nodejs.org/api/esm.html

## 4. The Node runtime and its event loop in depth

**Learned when:** the Learner predicts the output order of code mixing `process.nextTick`, promises, `setTimeout`, `setImmediate` and I/O callbacks, and explains why a CPU-heavy handler stalls every other request.

**Teach:** Node = V8 + libuv + the standard library; the event loop phases in order: timers, pending callbacks, poll, check (`setImmediate`), close callbacks; microtasks: `process.nextTick` queue drains before the promise microtask queue, and both drain between every callback; `setImmediate` vs `setTimeout(0)` inside an I/O callback; the thread pool for file system and DNS work; blocking the loop: a synchronous loop or `JSON.parse` on a huge string stalls all requests; `worker_threads` for CPU-bound work; streams and backpressure in one sentence; unhandled rejections crash the process.

**Probe:** thinking Node is multithreaded because "async"; expecting `setTimeout(fn, 0)` to run before a resolved promise's callback; believing `await` frees the CPU during a synchronous computation; thinking a slow database query blocks the event loop.

**Practice:** In the project, add a `/slow` route that does a CPU-bound loop for 3 seconds and a `/fast` route that returns immediately; hit `/slow` then `/fast` in two terminals and watch `/fast` wait. Then move the loop into a worker thread and repeat. It works when `/fast` answers instantly during the second run.

**Sources:** https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick

## 5. HTTP: methods, status codes, headers, cookies, cache headers, CORS

**Learned when:** the Learner reads a raw request and response, chooses the right method and status for an operation, and explains why a browser blocked a cross-origin call while `curl` succeeded.

**Teach:** request line, headers, body; methods and their promises: safe, idempotent (GET, PUT, DELETE), not idempotent (POST), partial update (PATCH); status classes 2xx/3xx/4xx/5xx and the ones to know by heart (200, 201, 204, 301/302, 304, 400, 401, 403, 404, 409, 422, 429, 500, 503); `Content-Type`, `Accept`, `Authorization`, `Location`; cookies: `Set-Cookie` attributes `HttpOnly`, `Secure`, `SameSite`, `Path`, `Max-Age`; caching: `Cache-Control` (`max-age`, `no-store`, `private`), `ETag` and `If-None-Match` → 304; CORS: same-origin policy, `Origin`, `Access-Control-Allow-Origin`, preflight `OPTIONS` for non-simple requests, credentials and why `*` won't do.

**Probe:** returning 200 with an error body; using 401 for "not allowed" and 403 for "not logged in"; thinking CORS is enforced by the server rather than the browser; `no-cache` read as "never cache"; believing cookies are sent to every domain; thinking PUT and POST are interchangeable.

**Practice:** With `curl -v` against the project (or any public API), send one request per method, force a 304 with `If-None-Match`, and trigger a CORS preflight from a browser page on a different port; read every header out loud. It works when the Learner can state, for each response, why the server chose that status and those headers.

**Sources:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview; https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS; https://www.rfc-editor.org/rfc/rfc9110.html

## 6. REST API design: resources, errors, pagination, versioning, OpenAPI

**Learned when:** the Learner designs a resource-based API on paper for a new domain, with consistent URLs, error shapes and pagination, and writes it as an OpenAPI document before any code.

**Teach:** resources as nouns, collections and items (`/orders`, `/orders/{id}`), nested resources sparingly; actions that aren't CRUD; consistent naming and plural nouns; a single error envelope (code, message, details, request id) and mapping errors to statuses; validation errors listing every failing field; pagination: offset vs cursor and why cursors survive inserts; filtering and sorting via query parameters; versioning (`/v1`) and what counts as a breaking change; OpenAPI 3.x as the contract: paths, operations, schemas, components, examples; generating docs from the spec.

**Probe:** verbs in URLs (`/getOrders`); one error format per endpoint; offset pagination on a busy table; leaking database ids or internals in responses; changing a response field's type and calling it "minor".

**Practice:** Write `openapi.yaml` for the Practice Project (Topic 17): at least three resources, list endpoints with cursor pagination, a shared error schema, and one example per response. It works when the document loads in an OpenAPI viewer (for example Swagger Editor) without validation errors and a peer could implement the API from it alone.

**Sources:** https://spec.openapis.org/oas/latest.html; https://www.rfc-editor.org/rfc/rfc9110.html

## 7. Building the API with Express in TypeScript

**Learned when:** the Learner builds an Express 5 app with routers per resource, ordered middleware, an error handler that catches thrown and rejected errors, and explains the request's path through the stack.

**Teach:** `express()`, `app.use`, `express.json()`; routers per resource and mounting; middleware as a chain: order matters, `next()`, `next(err)`; Express 5 specifics: rejected promises from async handlers go to the error handler automatically, route syntax changes (`/*splat`, `{optional}`), `req.query` is read-only, `req.body` is `undefined` without a parser; the four-argument error middleware placed last; a typed `HttpError` with a status; 404 handler; typing `req.params` and `req.body`; graceful shutdown on SIGTERM; Hono and Fastify as alternatives with the same shape (routing, middleware, error handling).

**Probe:** registering the error handler before the routes; wrapping every async handler in try/catch out of Express 4 habit; sending a response twice; trusting `req.body` types because they are annotated; `app.listen` without handling the error event.

**Practice:** Build the skeleton of the Practice Project: `/health`, one resource router with in-memory storage, request logging middleware, a 404 handler and a central error handler that turns a thrown `HttpError` into the error envelope from Topic 6. It works when an `async` handler that throws returns a JSON 500 (not a hung request) and an unknown path returns the 404 envelope.

**Sources:** https://expressjs.com/en/guide/migrating-5.html; https://expressjs.com/en/guide/using-middleware.html; https://expressjs.com/en/guide/error-handling.html

## 8. Validating input at trust boundaries (Zod)

**Learned when:** the Learner validates every body, query and path parameter with a Zod schema at the edge, derives the TypeScript type from the schema, and returns a 400/422 listing all invalid fields.

**Teach:** trust boundaries: the request, environment variables, third-party responses; Zod 4: `z.object`, `z.string`, `z.number`, `z.email()`, `z.enum`, `z.array`, `.optional()`, `.default()`; `safeParse` vs `parse`; `z.infer<typeof schema>` so types come from one place; unknown keys are stripped by default, `z.strictObject` rejects them, `z.looseObject` keeps them; `z.coerce` for query strings and ids; formatting errors with `z.flattenError` or `z.treeifyError` into the error envelope; validating `process.env` at startup; a reusable `validate(schema)` middleware; JSON.parse errors also need handling.

**Probe:** validating in the service layer instead of at the edge; declaring a type with `as` and calling it validated; forgetting query values are always strings; returning only the first validation error; using the same schema for create and update without `.partial()`.

**Practice:** Add Zod schemas for every input of the Practice Project's first resource, a `validate` middleware, and an env schema that fails fast on boot. It works when a request with two bad fields returns one 400 that names both, and starting the app without `DATABASE_URL` exits with a clear message.

**Sources:** https://zod.dev/api; https://zod.dev/error-formatting

## 9. Relational modeling: tables, keys, relationships, normalization

**Learned when:** the Learner turns a plain-language domain into tables with primary keys, foreign keys and constraints, chooses the relationship type for each pair of entities, and spots a normalization problem in a given schema.

**Teach:** entities become tables, attributes become columns; primary keys (integer identity vs UUID) and why they never change; foreign keys and referential integrity; one-to-many, many-to-many via a join table, one-to-one; `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`; `ON DELETE` choices; normalization in practice: no repeating groups, no facts stored twice, every non-key column depends on the key; when to denormalize on purpose; naming conventions; timestamps `created_at`/`updated_at`; enum-like columns.

**Probe:** storing a comma-separated list in a column; duplicating a customer's name on every order; making natural data (email) the primary key; missing the join table for many-to-many; nullable foreign keys used to mean "not set yet" without saying so.

**Practice:** Draw (text or diagram) the schema for the Practice Project: at least four tables, one many-to-many, foreign keys with explicit `ON DELETE` behavior, and constraints for every business rule you can name. Then write it as `CREATE TABLE` statements and run them against a local Postgres. It works when an insert that violates a rule is rejected by the database, not by app code.

**Sources:** https://www.postgresql.org/docs/current/ddl-constraints.html; https://www.postgresql.org/docs/current/tutorial-sql.html

## 10. SQL: SELECT, JOIN, GROUP BY, subqueries

**Learned when:** the Learner answers a business question by writing the SQL unaided, including a join across three tables, an aggregate with `GROUP BY`/`HAVING`, and a subquery or CTE.

**Teach:** logical order of evaluation: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT; `INNER` vs `LEFT` join and what rows disappear; joining through a join table; aggregates and `GROUP BY` rules; `HAVING` vs `WHERE`; `DISTINCT`; subqueries in `WHERE` (`IN`, `EXISTS`) and in `FROM`; CTEs (`WITH`) for readability; `INSERT ... RETURNING`, `UPDATE`, `DELETE` with `WHERE`; `NULL` three-valued logic; parameterized queries and why string concatenation is an injection.

**Probe:** `WHERE` on an aggregate; expecting `LEFT JOIN` to keep the left row after a `WHERE` on the right table's column; `NULL = NULL` treated as true; counting with `COUNT(column)` vs `COUNT(*)`; an `UPDATE` without `WHERE`.

**Practice:** Seed the Practice Project schema with a few dozen rows and write five queries that answer real questions (top customers by spend, items never ordered, monthly totals, latest order per customer, a search). It works when each result is checked by hand against the seed data and the Learner can explain which rows a `LEFT JOIN` added.

**Sources:** https://www.postgresql.org/docs/current/tutorial-sql.html

## 11. How databases work inside

**Learned when:** the Learner explains, for one `INSERT` and one indexed `SELECT`, what happens on disk and in memory: pages, the B-tree walk, the WAL write, and why a reader never blocks a writer in Postgres.

**Teach:** tables as heap files of fixed-size pages (8 kB); rows as tuples in pages; the buffer cache; B-tree indexes: sorted keys, log-depth tree, pointing to tuple locations; why an index costs writes; the write-ahead log: append the change first, then the page, so a crash can replay; checkpoints; MVCC: each tuple carries the transaction ids that created and deleted it, readers see a snapshot, updates create a new tuple version; dead tuples and `VACUUM`; sequential scan vs index scan cost intuition.

**Probe:** thinking an index is a copy of the table; believing writes go straight to the table file; assuming a `SELECT` locks rows; thinking an `UPDATE` changes the row in place; believing "the data is in memory" means durable.

**Practice:** On the local Postgres, create a table with 1 million rows, compare `SELECT` timing with and without an index on a filtered column, then watch `pg_stat_user_tables` `n_dead_tup` grow after a bulk `UPDATE` and shrink after `VACUUM`. It works when the Learner can explain each number seen.

**Sources:** https://www.postgresql.org/docs/current/storage-page-layout.html; https://www.postgresql.org/docs/current/wal-intro.html; https://www.postgresql.org/docs/current/mvcc-intro.html

## 12. Indexes, reading query plans (EXPLAIN), and the N+1 query problem

**Learned when:** the Learner reads an `EXPLAIN ANALYZE` plan, names the node that dominates the cost, adds the index that fixes it, and rewrites an N+1 loop as one query.

**Teach:** `EXPLAIN` vs `EXPLAIN ANALYZE` (the latter runs the query); plan nodes: Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan, Nested Loop, Hash Join, Merge Join, Sort; estimated vs actual rows and what a large mismatch means (stale statistics, `ANALYZE`); when the planner ignores an index (small tables, low selectivity, functions on the column); composite indexes and column order; partial and unique indexes; covering columns; the N+1 problem: one query for the list plus one per item, fixed with a join or `WHERE id IN (...)`; measuring before indexing.

**Probe:** indexing every column; expecting an index to help `WHERE lower(email) = ...`; reading cost units as milliseconds; thinking an ORM prevents N+1; adding an index without checking write cost.

**Practice:** In the Practice Project, write the list endpoint naively with a query per row, log the SQL, count the queries, then fix it with a join; separately, take the slowest query from Topic 10, read its plan, and add the one index that changes the scan type. It works when the query count drops to one and the plan shows the index being used with lower actual time.

**Sources:** https://www.postgresql.org/docs/current/using-explain.html; https://www.postgresql.org/docs/current/indexes.html; https://use-the-index-luke.com/

## 13. Transactions and isolation levels

**Learned when:** the Learner wraps a multi-step write in a transaction, explains what each Postgres isolation level prevents, and describes a lost-update scenario and two ways to prevent it.

**Teach:** `BEGIN`/`COMMIT`/`ROLLBACK`; atomicity: all or nothing; a transaction per request-level unit of work; anomalies: dirty read, non-repeatable read, phantom, lost update; Postgres levels: Read Committed (default, per-statement snapshot), Repeatable Read (per-transaction snapshot; in Postgres also blocks phantoms), Serializable (may fail with a serialization error and must be retried); `SELECT ... FOR UPDATE` and optimistic concurrency with a version column; keeping transactions short; deadlocks and how Postgres resolves them.

**Probe:** thinking Read Committed prevents two requests from both decrementing the same stock; believing a transaction makes code single-threaded; holding a transaction open across an external HTTP call; catching a serialization failure and not retrying.

**Practice:** In the Practice Project, implement a "transfer" or "reserve stock" operation, then hit it with 20 concurrent requests using a small script; watch it over-sell, then fix it with `FOR UPDATE` or a version check inside a transaction. It works when the final count is right after every run.

**Sources:** https://www.postgresql.org/docs/current/transaction-iso.html; https://www.postgresql.org/docs/current/tutorial-transactions.html

## 14. Using Postgres from Node: Drizzle, migrations, running Postgres locally with Docker Compose

**Learned when:** the Learner runs Postgres from a `compose.yaml`, defines the schema in Drizzle, generates and applies a migration, and writes typed queries and a transaction through the ORM.

**Teach:** `compose.yaml` with a `postgres` service, a named volume for data, environment for credentials, a port mapping; `docker compose up -d`, `logs`, `down`; `DATABASE_URL`; Drizzle setup: `drizzle-orm` + `drizzle-kit` + the `pg` driver, `drizzle.config.ts` (schema path, `out`, `dialect: "postgresql"`); `pgTable` and column builders, references, indexes in code; `drizzle-kit generate` → SQL migration files in git, `drizzle-kit migrate` to apply, `push` only for throwaway prototyping; `migrate()` at startup as an option; the query builder (`select`, `insert().values().returning()`, `update`, `delete`, `eq`, `and`), relations or joins; `db.transaction`; a connection pool and closing it on shutdown; never editing an applied migration.

**Probe:** using `push` in a shared or production database; hand-editing a generated migration that was already applied; opening a new connection per request; trusting the ORM to make N+1 impossible; committing the database volume or credentials.

**Practice:** Replace the in-memory store from Topic 7 with Drizzle: bring up Postgres with Compose, write the schema from Topic 9 in `schema.ts`, generate and apply the first migration, and port the resource routes. It works when `docker compose down && up` keeps the data, and a fresh clone reaches a working database with `migrate` alone.

**Sources:** https://orm.drizzle.team/docs/get-started/postgresql-new; https://orm.drizzle.team/docs/migrations; https://docs.docker.com/compose/gettingstarted/

## 15. Authentication fundamentals: password hashing, sessions and cookies vs tokens, CSRF

**Learned when:** the Learner implements signup and login with properly hashed passwords and a server-side session in an `HttpOnly` cookie, and explains the CSRF risk and the defense they chose.

**Teach:** authentication vs authorization; never store passwords: slow, salted hashes (argon2id first choice, bcrypt acceptable, `crypto.scrypt` built in) and why fast hashes fail; timing-safe comparison; sessions: random id in a cookie, state on the server (table or Redis), expiry and rotation on login; cookie flags `HttpOnly`, `Secure`, `SameSite=Lax`; tokens (JWT): stateless, signed, hard to revoke, where to store them and why `localStorage` is exposed to XSS; choosing sessions for a browser app; CSRF: cookies are sent automatically, so a foreign site can submit forms; defenses: `SameSite`, checking `Origin`, a CSRF token; generic error messages on login; rate limiting login attempts (details in Phase 6).

**Probe:** storing a SHA-256 of the password; keeping a JWT in `localStorage` "because cookies are old"; thinking `SameSite` alone is enough everywhere; returning "wrong password" vs "no such user"; forgetting to invalidate sessions on logout or password change.

**Practice:** Add `/auth/signup`, `/auth/login`, `/auth/logout` and a `requireAuth` middleware to the Practice Project using hashed passwords and a sessions table. It works when the password column contains only hashes, a protected route returns 401 without the cookie and 200 with it, and logout makes the old cookie useless.

**Sources:** https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html; https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html; https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

## 16. Logging and configuration

**Learned when:** the Learner's API emits one structured JSON log line per request with a request id and level, reads all configuration from validated environment variables, and behaves differently in development and production without code changes.

**Teach:** why `console.log` is not logging: levels, structure, machine-readable JSON; a logger such as pino: child loggers, request id per request, pretty printing only in development; what to log (method, path, status, duration, user id) and what never to log (passwords, tokens, full bodies); logging errors with stack traces once, at the boundary; configuration from the environment (12-factor), `.env` for local only, `.env.example` committed; the env schema from Topic 8; `NODE_ENV`; secrets never in git; log output to stdout and let the platform collect it.

**Probe:** logging inside every function so an error appears five times; writing logs to a file in the container; putting secrets in `config.ts`; treating `NODE_ENV=production` as a switch that changes correctness; logging request bodies with passwords.

**Practice:** Add pino with a request-logging middleware that assigns a request id and logs status and duration, and make the error handler log once with the stack. It works when one request produces exactly one JSON line in production mode and the request id appears in both the log and the error response.

**Sources:** https://getpino.io/; https://12factor.net/config

## 17. Practice Project: a REST API with Postgres

**Learned when:** the Learner ships a small but complete REST API (Express 5, Zod, Drizzle, Postgres, sessions, structured logs, OpenAPI document) from a public repo that a stranger can clone and run with `docker compose up` and `npm run dev`, and can explain any file in it.

**Teach:** choosing a domain with at least four related tables; folder structure: routes, services, db, schemas; the request path: middleware → validation → service → Drizzle → response envelope; pagination and filtering on list endpoints; ownership checks (users only see their own data); consistent errors; migrations in git; a README with setup steps and the OpenAPI file; a seed script; a short smoke test script with `curl` or a `.http` file; what "done" means: every endpoint in the spec works as documented.

**Probe:** business logic in route handlers; validation that lives in the service; endpoints not in the spec, or spec not matching the code; a README that only works on the author's machine; secrets committed by accident.

**Practice:** Build the API end to end over the last week of the Phase, then hand the repo to the Tutor's fresh-clone test: follow the README exactly on a clean checkout. It works when every OpenAPI operation returns the documented status and shape, an unauthenticated request cannot read another user's data, and the whole setup runs from the README alone.

**Sources:** https://expressjs.com/en/guide/error-handling.html; https://orm.drizzle.team/docs/migrations; https://spec.openapis.org/oas/latest.html
