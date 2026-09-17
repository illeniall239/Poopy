# Phase 8 — System design basics and interview preparation

30 hours over about 2 weeks, 8 Topics. At the end the Learner reasons through a junior-level system design question out loud, from requirements to a diagram with named trade-offs, and presents three portfolio projects and a work history convincingly.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: Explain-back, later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during Explain-back and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and notes, not in-app Exercises. Says what to produce and how the Learner knows it holds up.
- **Sources** — the pages the Tutor teaches against; current on 2026-09-17. Book chapters named in the Map (Kleppmann; Xu) are read alongside them.

---

## 1. Requirements gathering and back-of-the-envelope estimation

**Learned when:** given a one-line prompt ("design a photo-sharing app"), the Learner asks the right clarifying questions, writes functional and non-functional requirements, and estimates traffic, storage and bandwidth to the right order of magnitude in under ten minutes.

**Teach:** functional requirements (what users do) vs non-functional (scale, latency, availability, consistency, cost); asking about users, reads vs writes, data size, growth, and what "fast" means; the numbers to carry in your head: seconds per day (~86,400, round to 10⁵), bytes per character, a typical row or image size, requests per second from daily actives; QPS = daily actions / 10⁵, peak = 2–3×; storage per year; read/write ratio driving the design; stating assumptions out loud and writing them down; scoping to a core flow first.

**Probe:** jumping to boxes before requirements; estimating to the byte instead of the power of ten; treating every system as Twitter-scale; forgetting peak vs average; not asking about consistency needs; silence while thinking.

**Practice:** For three prompts (URL shortener, chat, news feed), write a one-page requirements and estimation sheet each, timed at ten minutes, then compare against the Tutor's numbers. It works when each estimate lands within an order of magnitude and every assumption is written before the design starts.

**Sources:** https://roadmap.sh/system-design; https://github.com/donnemartin/system-design-primer

## 2. Scaling stateless services: load balancers, horizontal scaling

**Learned when:** the Learner takes a single-server app to N instances behind a load balancer, identifies every place state was hiding (sessions, uploads, in-memory caches, WebSocket connections), and moves it out.

**Teach:** vertical vs horizontal scaling and where vertical stops; a stateless process: any instance can serve any request (12-factor processes); load balancer roles: distributing requests, health checks, TLS termination, layer 4 vs layer 7; algorithms: round robin, least connections, consistent hashing when affinity matters; sticky sessions as a smell; state that must move: sessions to Redis or the database, files to object storage, caches to Redis, real-time connections via pub/sub (Phase 6); autoscaling on CPU or queue depth; rolling deploys and health checks; the database as the next bottleneck; what the Learner already did in Phases 5 and 6 seen through this lens.

**Probe:** thinking a load balancer makes the app faster; in-memory sessions with two instances; assuming the database scales because the app did; sticky sessions as the fix for shared state; no health check so a dead instance still receives traffic.

**Practice:** Draw Portfolio Project 2 at 1 instance, 3 instances and 30 instances, listing at each step what breaks and what moves; then actually run it at two instances behind a tiny reverse proxy locally and confirm sessions, uploads and live updates still work. It works when the Learner can name each piece of state and where it lives at 30 instances.

**Sources:** https://12factor.net/processes; https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html; https://github.com/donnemartin/system-design-primer#load-balancer

## 3. Databases at scale: replication, read replicas, partitioning

**Learned when:** the Learner explains primary/replica replication, routes reads to replicas while naming the stale-read risk, and chooses a partition key for a given table with its hot-spot and cross-partition trade-offs.

**Teach:** a single Postgres goes far: indexes, connection pooling, caching first; replication: one primary takes writes, streaming WAL to replicas (Phase 3 Topic 11 pays off), synchronous vs asynchronous and replication lag; read replicas for read-heavy loads and read-your-own-writes problems; failover and promotion; vertical scaling of the primary; partitioning (sharding) when writes or data exceed one machine: choose a key (user id, tenant, time), hash vs range, hot partitions, cross-shard joins and transactions become application problems, rebalancing; Postgres declarative partitioning within one server as the first step; when to reach for a different store (key-value, document, search) and what you give up; backups and point-in-time recovery.

**Probe:** sharding as the first move; reading your own write from a lagging replica and calling it a bug in Postgres; a partition key that puts all today's data on one shard; expecting joins across shards to just work; synchronous replication "for safety" with no latency thought.

**Practice:** For Portfolio Project 1's schema, write a one-page scaling plan: which tables grow, when a read replica helps and which queries can tolerate lag, and the partition key for the largest table with its downsides; then set up a local streaming replica in Compose and observe lag under a write loop. It works when the Learner can show a stale read on the replica and explain two ways to handle it.

**Sources:** https://www.postgresql.org/docs/current/high-availability.html; https://github.com/donnemartin/system-design-primer

## 4. Caching strategies and CDNs

**Learned when:** the Learner places caches at each layer of a design (browser, CDN, application, database) with a named strategy and invalidation rule for each, and explains what a CDN does and does not cache.

**Teach:** the layers from Phase 6 Topic 5 generalized; strategies: cache-aside (lazy), read-through, write-through, write-behind, and their consistency; TTL vs event-driven invalidation; what to key on; eviction (LRU) and memory sizing; stampede protection; a CDN: edge servers near users caching static assets and cacheable responses, controlled by `Cache-Control` and purge APIs, plus TLS termination and DDoS absorption; what is CDN-cacheable (static files, public pages with `public, max-age`) and what isn't (per-user, `private`, `no-store`); Next.js static shell served from the CDN (Phase 4 Topic 8) as an example; measuring hit ratio; caching as the first answer to "too many reads".

**Probe:** caching personalized responses at the CDN; write-through everywhere "for consistency" without the write cost; a cache with no size limit; treating a cache miss storm as a database problem; invalidating by restarting Redis.

**Practice:** Annotate the news-feed design from Topic 1 with every cache: where, what key, TTL or invalidation, and expected hit rate; then check Portfolio Project 1's deployed asset headers with `curl -I` and fix any static asset not served with a long `max-age` and a content hash. It works when the CDN reports hits for assets and the design's read path never touches the database for the common case.

**Sources:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching; https://redis.io/docs/latest/develop/reference/eviction/; https://github.com/donnemartin/system-design-primer#cache

## 5. Queues and asynchronous architectures

**Learned when:** the Learner identifies which steps of a flow can leave the request path, designs them as producers, a queue and consumers with delivery guarantees and idempotency, and describes what the user sees while work is pending.

**Teach:** synchronous vs asynchronous work and the user-facing contract (202 Accepted, status endpoint, notification); queue roles: buffering bursts, decoupling, retries, fan-out; delivery semantics: at-most-once, at-least-once (the norm) and why exactly-once is application-level idempotency (Phase 6 Topic 4); ordering guarantees and partitions; dead letters and alerting; consumers scaling by queue depth; backpressure; event-driven designs: one event, many consumers, and the outbox pattern to publish reliably with a database write; where Redis/BullMQ stops and a log like Kafka begins (named, not taught); the trade-off: eventual consistency and harder debugging.

**Probe:** putting the queue in the request path and waiting on it; assuming order across consumers; no dead-letter plan; publishing an event before committing the row; a job that both charges a card and sends an email with one retry policy.

**Practice:** Redesign the checkout or notification flow of one portfolio project as an async architecture diagram: producers, queues, consumers, idempotency keys, dead letters, user status; then sketch the outbox table for it. It works when the Learner can walk through a consumer crash mid-job and a duplicate delivery without the user being charged twice.

**Sources:** https://github.com/donnemartin/system-design-primer#asynchronism; https://docs.bullmq.io/guide/retrying-failing-jobs

## 6. Consistency and availability trade-offs

**Learned when:** the Learner explains the CAP intuition without overstating it, names the consistency level a feature needs (strong, read-your-writes, eventual), and describes what a network partition does to a replicated system.

**Teach:** a distributed system is many machines that can fail and disagree; partitions happen, so during one you choose: refuse (consistency) or serve possibly stale data (availability); why "CAP" is a coarse tool and latency vs consistency is the everyday trade-off; consistency models a junior should name: linearizable/strong, read-your-writes, monotonic reads, eventual; where each fits: balances strong, a like counter eventual, a user's own profile read-your-writes; single-leader replication gives strong reads on the primary and eventual on replicas; leader election and split brain in one sentence; idempotency and retries as the tools for availability without duplicates; availability math: 99.9% is 8.7 hours a year, and dependencies multiply; SLOs and error budgets; timeouts, retries with backoff, circuit breakers, graceful degradation.

**Probe:** "we picked AP" as if databases have a switch; assuming a transaction on one node means consistency across nodes; retrying without timeouts; thinking 99.99% is cheap; believing eventual consistency means data loss.

**Practice:** For each feature of Portfolio Project 3 (chat history, approvals, retrieval index, billing counter), write the consistency level required and what happens during a partition between the app and the database or the agent service; then add one circuit breaker or timeout-with-fallback to the app and demonstrate it by killing the dependency. It works when the app degrades visibly instead of hanging and the table of consistency levels survives the Tutor's "what if two requests race" questions.

**Sources:** https://jepsen.io/consistency; https://github.com/donnemartin/system-design-primer#availability-vs-consistency

## 7. Designing classic systems: URL shortener, rate limiter, chat, news feed

**Learned when:** the Learner designs each of the four classic systems out loud in 35 minutes with a consistent method (requirements, estimates, API, data model, high-level diagram, deep dive on the hard part, trade-offs), and the design holds up to follow-up questions.

**Teach:** the method as a checklist and the clock; URL shortener: key generation (counter with base-62 vs hash vs pre-generated), redirects (301 vs 302 and analytics), read-heavy caching, expiry; rate limiter: where it sits (gateway vs service), algorithms (token bucket, sliding window), Redis atomicity, distributed counters, what to return (Phase 6 Topic 6 at scale); chat: WebSocket gateways, connection state, message storage and ordering, delivery receipts, fan-out to online and offline users, presence, pub/sub between gateways (Phase 6 Topics 1–2); news feed: fan-out on write vs on read and the celebrity problem, ranking, pagination by cursor, caching the feed, media via CDN; in each: the single hardest component to deep-dive; naming what you would build first for a small team vs at scale.

**Probe:** the same design for every prompt; skipping the API and data model; deep-diving the easy part; no numbers; never saying "it depends" with the dependency named; forgetting failure cases (gateway dies, Redis down).

**Practice:** Do four timed mock design sessions with the Tutor, one per system, drawing on paper or a whiteboard tool, and after each write a half-page retrospective of what was missed. It works when the fourth session covers every checklist step within time, and the Learner can answer three unplanned follow-ups (scale ×10, a failure, a new requirement) without restarting.

**Sources:** https://roadmap.sh/system-design; https://github.com/donnemartin/system-design-primer#system-design-interview-questions-with-solutions

## 8. Behavioral interviews (STAR), resume, and writing up portfolio projects

**Learned when:** the Learner tells six STAR stories from their own projects and experience in under two minutes each, has a one-page resume where every bullet states an outcome, and has three project write-ups a hiring manager can read in three minutes.

**Teach:** STAR: Situation, Task, Action (what you did, in the first person), Result (with a number or a concrete change); a story bank covering conflict, failure and what you learned, a hard technical problem, leading without authority, feedback, and shipping under constraints; mining the portfolio projects for stories (the transaction bug, the failed deploy, the red-team case); the resume: one page, reverse chronological, bullets as "did X with Y achieving Z", tech listed where used, links to the live projects and GitHub, no photo or full address; the GitHub profile README; project write-ups: problem, what it does with a live link, architecture diagram, the hardest decision and its trade-off, what you would do next, numbers (tests, latency, cost); answering "tell me about yourself" in 90 seconds; questions to ask the interviewer; salary and offer basics; following up.

**Probe:** stories told as "we" with no personal action; results without numbers; a resume listing duties instead of outcomes; write-ups that are feature lists; badmouthing a past team; no questions for the interviewer.

**Practice:** Write the six STAR stories, the resume, the GitHub profile README and the three project write-ups, then run two full mock behavioral interviews with the Tutor recorded and reviewed. It works when a mock reviewer can retell each project's hardest decision after reading the write-up once, every resume bullet has an outcome, and each story lands within two minutes with a concrete result.

**Sources:** https://www.google.com/about/careers/applications/how-we-hire; https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
