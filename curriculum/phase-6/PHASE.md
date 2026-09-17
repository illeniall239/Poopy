# Phase 6 — Real-time features and background jobs — Portfolio Project 2

42 hours over about 2 weeks, 8 Topics. At the end the Learner adds work that happens outside the request/response cycle (live updates, queued jobs, caches, rate limits, uploads) safely, and ships it as a second portfolio project.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: Explain-back, later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during Explain-back and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-17.

---

## 1. WebSockets and Server-Sent Events

**Learned when:** the Learner implements a live-updating page twice, once with SSE and once with WebSockets, and picks one for a given feature with a reason (direction, reconnection, proxies, cost).

**Teach:** why polling hurts; SSE: one-way server→browser over plain HTTP, `text/event-stream`, the `data:`/`event:`/`id:`/`retry:` fields, `EventSource` in the browser, automatic reconnection with `Last-Event-ID`, works through most proxies, needs no library; WebSockets: full-duplex after an HTTP upgrade, `ws` on the server, the browser `WebSocket` API, messages as strings or binary, no automatic reconnection, heartbeats/ping to detect dead connections; authentication on connect (cookie or token in the upgrade or first message); fan-out: one event must reach every connected client, which is why the next Topic exists; backpressure and slow clients; scaling: connections are state, so one server holds them and a load balancer must not break them (sticky sessions or pub/sub).

**Probe:** choosing WebSockets for a one-way feed "because it's real-time"; expecting `EventSource` to send data; forgetting reconnection and duplicate events on WebSocket; sending a message to `wss` without any auth; assuming two API instances share their connection lists.

**Practice:** Add a live activity feed to a copy of Portfolio Project 1 with SSE (Express route streaming events with ids), then a chat-style box with `ws`, both authenticated by the session cookie. It works when opening two browsers shows updates in both within a second, killing the server and restarting it makes the SSE client resume without duplicates, and an unauthenticated connection is rejected.

**Sources:** https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events; https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications; https://github.com/websockets/ws

## 2. Pub/sub with Redis

**Learned when:** the Learner runs two API instances behind one entry point and every connected client on either instance receives every event, via Redis pub/sub, and explains what happens to a message nobody was listening to.

**Teach:** Redis as an in-memory data structure server; running it in `compose.yaml`; the Node client (`redis` or `ioredis`), separate connections for subscribing and for commands; `PUBLISH channel message`, `SUBSCRIBE`, `PSUBSCRIBE` patterns; channels are not keys; delivery is at-most-once: no persistence, a subscriber that is down misses the message; the fan-out pattern: request handler → `PUBLISH` → each instance's subscriber → its own WebSocket/SSE clients; message shape (JSON with a type and a version); when you need at-least-once: Redis Streams (`XADD`/`XREADGROUP`) or a queue (Topic 3); sharded pub/sub in cluster mode exists.

**Probe:** using the same Redis connection to subscribe and to run commands; expecting pub/sub to buffer messages for a reconnecting subscriber; treating pub/sub as a queue for work that must not be lost; publishing large payloads instead of ids; forgetting environment prefixes so staging and production share channels.

**Practice:** Run the API as two instances (two ports) with a tiny reverse proxy or two browser tabs pointed at each, add Redis to Compose, and route the Topic 1 events through `PUBLISH`/`SUBSCRIBE`. It works when a client connected to instance A sees an event created via instance B, and stopping a subscriber during a publish shows the message is gone (at-most-once) when it returns.

**Sources:** https://redis.io/docs/latest/develop/pubsub/; https://redis.io/docs/latest/develop/clients/nodejs/; https://redis.io/docs/latest/develop/data-types/streams/

## 3. Background job queues: retries, backoff, dead letters

**Learned when:** the Learner moves slow or failure-prone work (email, image processing, webhooks) out of the request into a BullMQ queue with a separate worker, configures retries with exponential backoff, and inspects and replays failed jobs.

**Teach:** why the request should not wait: latency, failures, crashes mid-work; BullMQ on Redis: `Queue.add(name, data, opts)`, a `Worker` process with a processor function and `concurrency`; job lifecycle: waiting, active, completed, failed, delayed; `attempts` and `backoff: { type: 'exponential' | 'fixed', delay, jitter }`; the failed set as BullMQ's dead-letter equivalent: inspect, `retry()`, `removeOnComplete`/`removeOnFail` policies; stalled jobs when a worker dies; `QueueEvents` and progress; scheduling with `delay` and repeatable jobs; the worker runs in its own process (and container) so a crash doesn't take the API down; graceful shutdown (`worker.close()`); logging the job id with every line.

**Probe:** running the worker inside the API process "for now"; unlimited retries with no backoff hammering a down service; thinking a job that threw is retried automatically without `attempts`; storing large payloads in the job instead of ids; retrying non-idempotent work (Topic 4); no alert when the failed set grows.

**Practice:** Add a "send welcome email" (or "generate report") job to the project: the API enqueues, a separate `worker.ts` processes it with `attempts: 5` and exponential backoff, and a tiny admin endpoint lists failed jobs and retries one. It works when the request returns instantly, killing the worker mid-job and restarting it completes the job, and a processor that always throws lands the job in the failed set after five attempts with growing delays visible in the logs.

**Sources:** https://docs.bullmq.io/guide/retrying-failing-jobs; https://docs.bullmq.io/guide/queues; https://docs.bullmq.io/guide/workers

## 4. Idempotency

**Learned when:** the Learner makes a payment-like `POST` and a job processor safe to run twice, using an idempotency key and a unique constraint, and explains which HTTP methods are idempotent by contract and which their code must make so.

**Teach:** at-least-once delivery means everything retried can run twice: network retries, queue retries, double clicks; idempotent by definition: GET, PUT, DELETE; POST is not, so make it so: client-generated `Idempotency-Key` header, stored with the response, replayed on repeat; database enforcement: a unique constraint on the key (or on the natural key like `order_id` + `event_type`) and `INSERT ... ON CONFLICT DO NOTHING`; the "check then act" race and why the constraint, not the check, is the guarantee; idempotent job processors: BullMQ `jobId` to deduplicate enqueues, a processed-events table for webhooks; exactly-once as a lie; designing operations as "set to X" rather than "add 1".

**Probe:** checking `if (!exists) insert` without a constraint and calling it safe; putting the idempotency key in the body where a retry may not include it; keeping keys forever or for a second; making DELETE return 404 on the second call and calling that a bug; assuming the queue guarantees a job runs once.

**Practice:** Add an `Idempotency-Key` requirement to the project's most important `POST`, backed by a table with a unique key that stores the first response, and give the Topic 3 job a natural `jobId`. It works when sending the same request 20 times in parallel with a script creates exactly one record and returns the same response, and enqueuing the same job twice runs it once.

**Sources:** https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header; https://docs.bullmq.io/guide/jobs/job-ids; https://www.rfc-editor.org/rfc/rfc9110.html

## 5. Caching: Redis caching and invalidation

**Learned when:** the Learner caches an expensive read in Redis with a TTL, invalidates it on write, measures the hit rate, and can explain the difference between this application cache and the HTTP caching from Phase 3 and the Next.js cache from Phase 4.

**Teach:** the layers: browser/CDN (HTTP `Cache-Control`, `ETag`), framework (`'use cache'`), application (Redis), database (buffer cache); cache-aside: read → miss → compute → `SET key value EX ttl` → return; key design with a version prefix; TTL as the safety net, explicit invalidation (`DEL` on write) as the precision tool; the two hard problems: invalidation (stale reads after a write) and stampedes (many misses at once: lock, early refresh or jitter); what not to cache (per-user secrets without a per-user key, anything that must be fresh); serialization cost; memory limits and eviction policies (`allkeys-lru`); measuring: hits, misses, p95 with and without; cache warming; the Next.js `'use cache: remote'` handler as the same idea inside the framework.

**Probe:** caching with no TTL "because we invalidate"; invalidating one key but not the list that contains it; treating Redis as the source of truth; a key without a version so a shape change poisons every reader; caching the whole response for all users under one key; skipping measurement.

**Practice:** Cache the project's slowest list query in Redis with a 60-second TTL and delete the key in the write path, then load-test the endpoint before and after with a small script and log hits/misses. It works when the p95 drops visibly, a write is reflected on the next read, and the hit ratio is printed by a `/metrics`-style endpoint.

**Sources:** https://redis.io/docs/latest/commands/set/; https://redis.io/docs/latest/develop/reference/eviction/; https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching

## 6. Rate limiting

**Learned when:** the Learner protects login and a costly endpoint with a Redis-backed rate limit shared across instances, returns 429 with `Retry-After`, and explains the algorithm they chose and its edge behavior.

**Teach:** why: abuse, brute force, cost, fairness; keying by user id or IP (and the proxy headers problem: `X-Forwarded-For`, `trust proxy`); algorithms: fixed window (`INCR` + `EXPIRE`, bursty at edges), sliding window log or counter, token bucket (smooth, allows bursts); atomicity with `MULTI` or a Lua script; per-route limits (login tighter than reads); the response: 429, `Retry-After`, `RateLimit-*` headers; fail open or closed when Redis is down and why login should fail closed; limits in the worker for outbound APIs; observability of rejections.

**Probe:** an in-memory limiter on a multi-instance app; keying only by IP behind a proxy so everyone shares one bucket, or trusting `X-Forwarded-For` blindly; `INCR` then `EXPIRE` as two calls that can leave a key without a TTL; returning 403 instead of 429; no limit on login.

**Practice:** Add a Redis fixed-window limiter as Express middleware (atomic with a Lua script or `MULTI`), apply 5/minute to login and 100/minute to the API per user, with 429 and `Retry-After`. It works when a loop of 10 login attempts gets five 429s with the right header, the limit holds across two API instances, and the counter key always has a TTL in `redis-cli`.

**Sources:** https://redis.io/docs/latest/develop/use/keyspace/; https://redis.io/docs/latest/commands/set/; https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

## 7. File uploads and object storage (S3-compatible)

**Learned when:** the Learner lets users upload an image straight to S3-compatible storage with a presigned URL, stores only the key in Postgres, serves it back safely, and processes it in a background job.

**Teach:** why files don't belong in Postgres or on the app server's disk; object storage: buckets, keys, objects, metadata, the S3 API as the de-facto standard (AWS S3, Cloudflare R2, MinIO locally in Compose); presigned PUT URLs so the browser uploads directly and the API never proxies bytes; constraints on the presign (content type, size limit, key under the user's prefix); the flow: request presign → upload → confirm → row with key, size, type; validating type by content, not by extension; private buckets with presigned GET or a CDN in front; a BullMQ job to resize or scan after upload; deleting objects when the row is deleted; never trusting the client's file name.

**Probe:** streaming uploads through the API "to validate them"; a public bucket "for simplicity"; storing the full URL instead of the key; trusting `Content-Type` from the browser; unbounded presign expiry; keys built from user-supplied names (path traversal, collisions).

**Practice:** Add avatar upload to the project with MinIO in Compose: presigned PUT limited to images under 2 MB, a confirm endpoint that records the key, a job that makes a thumbnail, and presigned GET for display. It works when the browser uploads without touching the API, a `.exe` renamed to `.png` is rejected at confirm, and deleting the user removes both objects.

**Sources:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html; https://min.io/docs/minio/container/index.html

## 8. Portfolio Project 2: an app with real-time updates and background jobs

**Learned when:** the Learner ships a second deployed project whose core feature depends on live updates and queued work (for example a collaborative board, an order tracker or a notification center), with a worker, Redis, idempotent writes, rate limits and a diagram that explains the moving parts.

**Teach:** choosing a domain where async is the point, not a bolt-on; the architecture: API, worker, Redis (pub/sub, queue, cache, limits), Postgres, object storage, SSE or WebSocket gateway; running all of it locally with Compose and in production as separate services; failure drills: kill the worker, kill Redis, disconnect the client, and what the user sees; idempotency and retries everywhere something can run twice; observability for async work: job ids in logs, failed-set alert, connection counts; README with the diagram, the failure drills and their outcomes; reusing Project 1's auth, tests and CI rather than rebuilding.

**Probe:** real-time as decoration on a CRUD app; a worker with no retry policy or alerting; jobs that are not idempotent; a Compose file that works locally with no production equivalent; skipping the failure drills.

**Practice:** Build, deploy and document the project over the second week, then run the three failure drills on the deployed app and record what happened. It works when the live feature updates across two browsers, a killed worker resumes its jobs, the app degrades gracefully with Redis down (or fails closed where it should), and CI runs the integration tests with Redis and Postgres services.

**Sources:** https://docs.bullmq.io/guide/workers; https://redis.io/docs/latest/develop/pubsub/; https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
