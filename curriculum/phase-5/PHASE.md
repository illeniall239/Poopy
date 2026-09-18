# Phase 5 — Security, testing, deployment — Portfolio Project 1

69 hours over about 4 weeks, 12 Topics. At the end the Learner ships a secure, tested, deployed full-stack app with CI and can defend every security decision in it to a reviewer.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: a passed Project Review, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-17.

---

## 1. OWASP Top 10:2025 applied

**Learned when:** the Learner audits their own Phase 3/4 code against the OWASP Top 10:2025, finds at least one real instance of three categories, and fixes each with the standard control rather than a patch.

**Teach:** A01 Broken Access Control: every handler checks who may touch this record (ownership, not just login), IDOR, CSRF as an access-control failure, SSRF (now inside A01) when the server fetches a user-supplied URL; A05 Injection: SQL via parameters only, command injection, XSS (React escapes text, `dangerouslySetInnerHTML` and `href="javascript:"` don't), output encoding per context; A02 Security Misconfiguration: default credentials, verbose errors in production, permissive CORS, missing security headers, Content Security Policy (`default-src 'self'`, nonces for inline scripts, report-only first); A03 Software Supply Chain Failures: lockfiles, `npm audit`, pinning, reviewing install scripts, Dependabot; A10 Mishandling of Exceptional Conditions: fail closed, no stack traces to clients, catch-all handlers that hide state; the rest of the list by name (A04 Cryptographic Failures, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures) and where the curriculum covers each.

**Probe:** thinking "logged in" equals "allowed"; trusting the ORM to make injection impossible in raw fragments; believing React makes XSS impossible; a CSP that includes `'unsafe-inline'` and is called "done"; `npm audit` fix with no lockfile review; returning 500 with the error message and stack in production "for debugging".

**Practice:** In the Portfolio Project repo, write `SECURITY-REVIEW.md` with one row per OWASP category (finding or "not applicable and why"), then fix the findings: add an ownership check to every write endpoint, a CSP header in report-only mode then enforced, and a CI step that fails on `npm audit --audit-level=high`. It works when a user's session cannot read or modify another user's record by changing an id, and the CSP report endpoint receives no violations from normal use.

**Sources:** https://top10.owasp.org/2025; https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html; https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

## 2. Authentication and authorization done properly

**Learned when:** the Learner replaces the hand-rolled Phase 3 sessions with an established auth library, adds "Sign in with GitHub or Google" via OAuth/OIDC, and enforces role-based access with a single authorization helper used by every route and Server Function.

**Teach:** why not hand-roll in production: password resets, verification, OAuth flows, rotation, timing attacks; OAuth 2.0 (delegated authorization) vs OIDC (identity on top of it): authorization code flow with PKCE, redirect URI, state, the id token, and what the app actually stores (its own user and session); an established TypeScript auth library (Better Auth with the Drizzle adapter, or Auth.js) wired to Postgres: email/password, social providers, sessions in cookies; authorization: roles and ownership, deny by default, one `can(user, action, resource)` function called in the handler, never only in the UI or Proxy; admin routes; protecting Server Functions and Route Handlers the same way; logout everywhere and session invalidation.

**Probe:** treating the OAuth access token as proof of identity; storing the provider's tokens in the browser; checking roles in the React component only; trusting a `role` field sent by the client; forgetting the callback URL allow-list; assuming a library removes the need for authorization logic.

**Practice:** Migrate the Portfolio Project to the chosen auth library with email/password plus one OAuth provider, add `user`/`admin` roles in the schema, and route every write through `can()`. It works when a normal user gets 403 on an admin endpoint via the API directly (not just a hidden button), signing in with the provider creates one linked user, and the old Phase 3 session code is deleted.

**Sources:** https://www.better-auth.com/docs/introduction; https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

## 3. Secrets and environment configuration

**Learned when:** the Learner's repo contains no secret in any commit, every secret lives in the platform's secret store (local `.env`, GitHub Actions secrets, host environment), and rotating one requires no code change.

**Teach:** what is a secret (API keys, database URLs with passwords, session signing keys, OAuth client secrets) and what is configuration (ports, feature flags, public URLs); one config module that validates `process.env` with Zod at startup (from Phase 3) and is the only place `process.env` is read; `.env.local`/`.env` git-ignored, `.env.example` committed; per-environment values (dev, CI, production) without branches in code; `NEXT_PUBLIC_` means public forever; GitHub Actions `secrets.*` and environments; rotating a leaked key: revoke first, then replace; scanning history for leaks and why `git rm` doesn't remove them; least privilege for database users and API keys.

**Probe:** a secret in a "private" repo counts as safe; putting a secret in `next.config.ts`; reading `process.env` all over the codebase; rotating a key by pushing a commit; thinking deleting the file removes it from history.

**Practice:** Audit the Portfolio Project: run a secret scanner (for example `gitleaks`) over the full history, move every secret into the config module and the right store, and add `.env.example`. It works when the scanner reports nothing, a fresh clone with the example file fails fast with a clear message naming the missing variables, and CI runs with secrets it reads from GitHub only.

**Sources:** https://12factor.net/config; https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html; https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions

## 4. Unit and integration testing with Vitest, including against a real database

**Learned when:** the Learner writes unit tests for pure logic and integration tests that hit a real Postgres through the API, keeps them isolated and fast, and explains what each layer of test can and cannot catch.

**Teach:** the test pyramid in practice: pure functions (unit), routes plus database (integration), browser (Topic 6); Vitest 5: `vitest.config.ts`, `describe`/`it`/`expect`, watch mode, `vi.fn()` and `vi.mock()` for modules you don't own, `vi.useFakeTimers()`; arrange-act-assert and one behavior per test; naming tests by behavior; integration setup: a test database from `compose.yaml`, migrations in `globalSetup`, truncate between tests or wrap each in a rolled-back transaction, a `supertest`-style call against the Express app without a network port; testing error paths and validation, not only happy paths; coverage as a hint, not a target; keeping tests deterministic (no real time, no network).

**Probe:** mocking the database in an integration test and calling it tested; tests that depend on order or on each other's rows; asserting on implementation details (which function was called) instead of behavior; sleeping in tests; 100% coverage as the goal; one giant test per endpoint.

**Practice:** Add Vitest to the Portfolio Project's API: unit tests for the `can()` helper and any pricing or validation logic, and integration tests for one resource's full CRUD plus its 400, 401, 403 and 404 paths against a real Postgres. It works when `npm test` passes in under 30 seconds from a fresh database, and deliberately breaking the ownership check makes a test fail.

**Sources:** https://vitest.dev/guide/; https://vitest.dev/guide/mocking.html; https://vitest.dev/config/

## 5. Component testing with React Testing Library

**Learned when:** the Learner tests React components the way a user experiences them (roles, labels, text, keyboard), covers loading, error and success states, and never queries by class name or implementation detail.

**Teach:** the Testing Library philosophy: tests resemble how users use the software; `render`, `screen`, the query priority (`getByRole` with `name` first, `getByLabelText`, `getByText`, `getByTestId` last); `getBy` throws, `queryBy` returns null for absence, `findBy` awaits; `userEvent` over `fireEvent` (typing, clicking, tabbing); asserting accessibility as a side effect (a button with no name fails the query); testing forms: validation messages appear, submit is disabled while pending; mocking `fetch` or the API client module at the boundary; jsdom vs Vitest browser mode; testing Client Components in isolation while Server Components are covered by integration and end-to-end tests.

**Probe:** `container.querySelector('.btn')`; asserting on state variables; using `getBy` to check something is absent; testing every prop combination instead of behaviors; snapshot tests of whole pages; thinking a green component test means the page works.

**Practice:** Test the Portfolio Project's create/edit form component: renders labeled fields, shows a validation message for an empty required field, disables the submit button while pending, and shows the server error text on failure. It works when each test finds elements only by role, label or text, and removing the input's `<label>` makes a test fail.

**Sources:** https://testing-library.com/docs/queries/about/; https://testing-library.com/docs/react-testing-library/intro/; https://testing-library.com/docs/user-event/intro

## 6. End-to-end testing with Playwright

**Learned when:** the Learner writes Playwright tests for the critical user journeys (sign up, sign in, create, see, delete) against the running app, keeps them stable with locators and web-first assertions, and runs them in CI.

**Teach:** what end-to-end tests are for: the few journeys that must never break; `@playwright/test`: `test`, `expect`, the `page` fixture with an isolated browser context per test; locators (`getByRole`, `getByLabel`, `getByText`) and auto-waiting; web-first assertions (`toBeVisible`, `toHaveText`, `toHaveURL`) that retry; `playwright.config.ts`: `webServer` to start the app, `baseURL`, projects for browsers; authentication once with `storageState` reused across tests; seeding or resetting the database per run; `npx playwright codegen` to draft, then clean up; the trace viewer and `--ui` mode for failures; keeping the suite small and fast.

**Probe:** `page.waitForTimeout(2000)`; CSS selectors tied to markup; one test that walks the whole app; sharing state across tests so order matters; running end-to-end tests against production data; treating a flaky test as "just retry".

**Practice:** Add Playwright to the Portfolio Project with three journeys: sign in and see the list, create an item and see it appear, delete it and confirm it is gone; log in once via `storageState`. It works when `npx playwright test` passes headless from a fresh database, and a trace opens for a deliberately broken selector.

**Sources:** https://playwright.dev/docs/writing-tests; https://playwright.dev/docs/intro; https://playwright.dev/docs/test-fixtures

## 7. CI with GitHub Actions

**Learned when:** the Learner's repo runs type-check, lint, unit, integration (with a Postgres service) and Playwright tests on every push and pull request, blocks merging on failure, and the workflow is readable by someone new.

**Teach:** `.github/workflows/ci.yml`; `on: [push, pull_request]`; `jobs`, `runs-on: ubuntu-latest`, `steps` with `uses` (`actions/checkout@v6`, `actions/setup-node` with `cache: npm`) and `run`; `npm ci` not `npm install`; a `services:` block for Postgres with a health check; environment variables and `secrets.*`; caching Playwright browsers; uploading the Playwright report as an artifact on failure; matrix builds only when needed; branch protection requiring the check; keeping CI under ten minutes by running jobs in parallel; pinning action versions.

**Probe:** installing with `npm install` in CI so the lockfile drifts; secrets echoed into logs; a workflow that only runs on `main`; skipping the database in CI and mocking instead; ignoring a red build "because it's flaky".

**Practice:** Write the CI workflow for the Portfolio Project with jobs `check` (tsc + lint), `test` (Vitest with a Postgres service) and `e2e` (Playwright with report artifact), and require them in branch protection. It works when a PR with a failing test cannot be merged, and the Playwright report is downloadable from the failed run.

**Sources:** https://docs.github.com/en/actions/writing-workflows/quickstart; https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions

## 8. How the cloud and deployment work

**Learned when:** the Learner explains the layers from physical server to serverless, places a PaaS, a container platform and a VM on that ladder with their trade-offs, and narrates everything that happens between `git push` and a live URL for their own app.

**Teach:** a data center rack of physical machines; virtual machines share hardware via a hypervisor; containers share a kernel and start in seconds; orchestration (Kubernetes) as "many containers on many machines," named but not used here; serverless functions: no server to manage, cold starts, execution limits; PaaS (Vercel, Render, Fly.io, Railway): you push code, they build, run and route; managed databases; the `git push` story: webhook → build (install, `next build`, image) → artifact → rollout with health checks → load balancer/CDN → DNS → TLS certificate; environments (preview, staging, production); rollbacks as redeploying an old artifact; the cost model of each layer; regions and latency.

**Probe:** thinking the cloud is "someone else's magic"; believing serverless means no limits; assuming a VM and a container isolate the same way; expecting a deploy to be instant and atomic everywhere; thinking a CDN caches dynamic pages by default.

**Practice:** Draw the deployment diagram for the Portfolio Project (browser → DNS → CDN/edge → app instances → managed Postgres, plus the build pipeline) and write a one-page "what happens on push" for the README. It works when the Learner can point at each box and say which company runs it, what fails if it goes down, and what a rollback touches.

**Sources:** https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/; https://nextjs.org/docs/app/getting-started/deploying; https://12factor.net/

## 9. Docker: images, containers, Compose

**Learned when:** the Learner writes a multi-stage `Dockerfile` for the API and for the Next.js app, runs the whole stack with one `docker compose up`, and explains layers, caching and why the image is small and runs as a non-root user.

**Teach:** image vs container; `Dockerfile` instructions: `FROM` an LTS Node image, `WORKDIR`, `COPY` lockfile first then `RUN npm ci` for layer caching, `COPY` the rest, `RUN npm run build`, multi-stage build so dev dependencies never ship, `USER node`, `EXPOSE`, `CMD`; `.dockerignore`; `docker build`, `run -p`, `logs`, `exec`; environment variables at run time, not baked in; `compose.yaml` with `api`, `web`, `db` services, `depends_on` with health checks, named volumes, the default network and service names as hostnames; `docker compose up --build`, `down -v`; Next.js `output: 'standalone'` for a small image; health check endpoints.

**Probe:** copying everything before `npm ci` so every change reinstalls; baking `.env` into the image; running as root; expecting `localhost` inside a container to reach another container; `docker compose down -v` in production; a 2 GB image with dev dependencies.

**Practice:** Dockerize both Portfolio Project services with multi-stage builds and extend `compose.yaml` so `docker compose up --build` brings up db, api and web with migrations applied. It works when the app is usable at `localhost:3000` from a clean machine with only Docker installed, each image is under a few hundred MB, and `docker exec` shows the process running as `node`.

**Sources:** https://docs.docker.com/reference/dockerfile/; https://docs.docker.com/compose/; https://docs.docker.com/compose/gettingstarted/

## 10. Deploying a full-stack app with a managed Postgres

**Learned when:** the Learner deploys the API and the Next.js app to a hosting platform with a managed Postgres, runs migrations safely on deploy, serves over HTTPS on a real domain, and can roll back.

**Teach:** choosing a platform (a PaaS for the Next.js app, a container host or the same PaaS for the API, a managed Postgres such as Neon, Supabase, RDS or the platform's own); production `DATABASE_URL` with SSL and a pooler; running `drizzle-kit migrate` as a release step before the new version takes traffic, and writing backward-compatible migrations (add column, backfill, then drop); environment variables per environment; custom domain, DNS records, automatic TLS; health checks and zero-downtime rollout; preview deployments per PR; rollback = redeploy the previous build, and why a migration can't always be rolled back; backups and a restore drill; cost limits and alerts.

**Probe:** running migrations from a laptop against production; a migration that drops a column the old version still reads; committing the production URL with credentials; assuming the platform backs up the database for you; deploying from `main` without CI passing; forgetting the `Secure` cookie flag now that it's HTTPS.

**Practice:** Deploy the Portfolio Project: managed Postgres, API and web app on a platform, migrations in the release step, a custom or platform domain over HTTPS, and one deliberate rollback. It works when the live URL passes the Playwright suite pointed at it, the database restore drill (restore a backup to a new instance and connect) succeeds, and the rollback restores the previous version within minutes.

**Sources:** https://nextjs.org/docs/app/getting-started/deploying; https://orm.drizzle.team/docs/migrations

## 11. Observability: structured logs, metrics, error tracking

**Learned when:** the Learner can answer "what happened to request X" and "is the app healthy right now" for the deployed app from logs, a few metrics and an error tracker, without SSH-ing anywhere.

**Teach:** the three signals: logs (events with context), metrics (numbers over time), traces (one request across services); structured logs from Phase 3 shipped to the platform's log viewer, searchable by request id and user id; the four golden signals (latency, traffic, errors, saturation) as the first dashboard; a `/health` endpoint that checks the database; error tracking (Sentry or similar) for exceptions with stack traces, breadcrumbs and release tags, front end and back end, with source maps; alerting on error rate and p95 latency, not on every log line; correlating a frontend error with the API request id; avoiding personal data in logs and error reports; OpenTelemetry as the vendor-neutral way to emit all three.

**Probe:** `console.log` debugging in production; alerting on everything then ignoring alerts; logging full request bodies with personal data; thinking uptime checks are observability; no request id so front and back can't be correlated; error tracking only on the client.

**Practice:** Add error tracking to both services with release tagging and source maps, wire the request id into the frontend error context, and set two alerts (5xx rate and p95 latency). It works when throwing a deliberate error on a hidden route shows up in the tracker with the correct release and the matching API log line, and the alert fires during a short load test.

**Sources:** https://opentelemetry.io/docs/concepts/signals/; https://docs.sentry.io/platforms/javascript/guides/nextjs/; https://getpino.io/

## 12. Portfolio Project 1: full-stack app with auth, Postgres, tests, CI, deployed

**Learned when:** the Learner presents a deployed full-stack app (Next.js 16 + Express 5 API + Postgres) with real authentication, authorization, tests at three levels, CI, Docker and observability, and can answer a reviewer's "why" on any security or architecture decision.

**Teach:** scoping a portfolio project to one clear domain and one user journey done well; the README as the pitch: what, live link, screenshots, architecture diagram, how to run, how it's tested, security notes; a `docs/decisions.md` with short entries (why sessions over JWT, why this auth library, why these tests); a demo account; the security review from Topic 1 kept current; a checklist before calling it done: CSP enforced, ownership checks tested, secrets scanned, CI green, deploy from `main` only, rollback tried, backups verified; explaining trade-offs out loud.

**Probe:** feature creep over finish; a README with no live link or no architecture; tests that exist but don't run in CI; security decisions the Learner can't justify beyond "the tutorial said so"; a deployed app with the dev database.

**Practice:** Finish and polish the Portfolio Project over the last week: README, decisions log, demo account, and a 10-minute walkthrough the Learner records or gives live. It works when the fresh-clone test passes, the live app passes the Playwright suite, and the Tutor's mock code review finds no OWASP Top 10 finding the Learner cannot explain or has not fixed.

**Sources:** https://top10.owasp.org/2025; https://docs.github.com/en/actions/writing-workflows/quickstart; https://nextjs.org/docs/app/getting-started/deploying
