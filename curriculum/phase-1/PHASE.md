# Phase 1 — Problem solving and TypeScript fundamentals

54 hours over 3 weeks, 15 Topics. For a Learner who can write basic scripts but freezes on a blank problem.

Every Topic below lists:
- **Learned when** — what the Learner must show, on top of the standard rule (Exercises pass without hints, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Exercises** — folder names under this directory, in order.

Exercise folder layout: `exercise.md` (problem, examples, Hint Ladder, and the questions the Breakdown answers), then per language a starter, a test and a reference: `starter.ts`/`test.ts`/`reference.ts` (TypeScript; JavaScript is derived from it), `starter.py`/`test.py`/`reference.py`, `starter.java`/`test.java`/`reference.java`. The reference is only used by `scripts/verify-exercises.mjs` to prove the tests are correct; it is shown in the Breakdown once the Learner's own solution passes. The problem text is written in TypeScript terms; the Tutor translates for other languages.

---

## 1. A method for solving problems

**Learned when:** before writing code, the Learner restates the problem, works 2+ examples by hand including an edge case, and writes a plain-language plan.

**Teach:** restating inputs and outputs; working examples by hand; finding the edge cases (zero, one, empty, huge, exact boundary); writing the steps in plain words; solving a smaller version first; checking the plan against the examples before coding.

**Probe:** starting to type before understanding; only testing the example given; treating "it runs" as "it's correct".

**Exercises:**
- `01-01-coin-change-greedy` — minimum coins for an amount using 25/10/5/1.
- `01-02-cinema-seat` — seat number → row and column.
- `01-03-snail-in-a-well` — days for a snail to climb out of a well.

## 2. Values, types, variables and expressions

**Learned when:** the Learner predicts the value and type of expressions, including integer division, remainder, number precision and basic string operations.

**Teach:** `number`, `string`, `boolean`; `const` vs `let`; type annotations, including everyday types for arrays (`number[]`) and objects (`{ name: string }`); arithmetic operators, `%`, `Math.floor`/`Math.round`; operator precedence; floating-point surprises (`0.1 + 0.2`); string basics: `length`, indexing, `slice`, `padStart`, concatenation, template literals. (Character-by-character processing comes in Topic 7.)

**Probe:** `/` doing integer division; `const` making values immutable; `==` vs `===`; string + number concatenation.

**Exercises:**
- `02-01-temperature-convert` — Celsius ↔ Fahrenheit, rounded to one decimal.
- `02-02-split-the-bill` — split a bill in cents with the remainder going to the first people.
- `02-03-seconds-to-clock` — seconds → `"HH:MM:SS"`.

## 3. Conditionals and boolean logic

**Learned when:** the Learner orders conditions correctly and simplifies boolean expressions without changing behavior.

**Teach:** `if`/`else if`/`else`; `&&`, `||`, `!`; short-circuiting; comparison operators; ordering overlapping conditions; truthy and falsy values.

**Probe:** order of overlapping conditions; truthiness of `0` and `""`; De Morgan's laws.

**Exercises:**
- `03-01-leap-year` — Gregorian leap year rule.
- `03-02-shipping-cost` — tiered shipping rules with overlapping thresholds.
- `03-03-triangle-kind` — classify a triangle or reject invalid sides.

## 4. Loops and tracing code by hand

**Learned when:** the Learner traces a loop in a table (variables per iteration) and fixes off-by-one errors by reasoning, not trial and error.

**Teach:** `for`, `while`, `for...of`; loop bounds; `break`/`continue`; tracing tables; what stays true on every iteration (invariant, informally); nested loops.

**Probe:** `<` vs `<=`; loops that never run or never stop; modifying a counter inside the body.

**Exercises:**
- `04-01-sum-of-multiples` — sum of numbers below n divisible by 3 or 5.
- `04-02-digit-sum-until-single` — repeatedly sum digits until one digit remains.
- `04-03-collatz-steps` — steps for the Collatz sequence to reach 1.

## 5. Functions and breaking problems down

**Learned when:** the Learner splits a problem into small named functions, each testable alone, and explains what each one promises.

**Teach:** parameters and return values; return vs side effects (printing); pure functions; naming; helper functions; early returns; scope: block scope, `let`/`const` vs `var`, hoisting.

**Probe:** confusing `console.log` with `return`; functions that do several unrelated things; mutating arguments; using a `var` or function before its line runs.

**Exercises:**
- `05-01-is-prime-and-next-prime` — `isPrime` and `nextPrime` built on it.
- `05-02-password-strength` — score a password from small rule-check helpers.
- `05-03-roman-numerals` — integer → Roman numeral.

## 6. Arrays and accumulator patterns

**Learned when:** the Learner names and applies the accumulator patterns (sum, count, max/min, filter into new array, build a result) without higher-order functions.

**Teach:** indexing; length; push; iterating with index vs `for...of`; accumulator patterns; not mutating the input; empty arrays.

**Probe:** `max` initialized to `0` with all-negative input; index out of range returning `undefined`; mutating the input array.

**Exercises:**
- `06-01-max-and-min` — largest and smallest value, with empty input handled.
- `06-02-running-average` — average after each element.
- `06-03-second-largest-distinct` — second largest distinct value.

## 7. Strings

**Learned when:** the Learner processes strings character by character and knows strings are immutable.

**Teach:** indexing; length; `slice`; `split`/`join`; building strings; case conversion; character comparison; immutability.

**Probe:** trying to assign `s[0] = "x"`; off-by-one in `slice` end index; case-sensitive comparisons.

**Exercises:**
- `07-01-is-palindrome` — ignoring case and non-letters.
- `07-02-compress-runs` — `"aaabcc"` → `"a3bc2"`.
- `07-03-caesar-cipher` — shift letters, keep case and other characters.

## 8. Objects, Map and Set

**Learned when:** the Learner chooses between an object, a `Map` and a `Set` for a job and explains why.

**Teach:** object literals and property access; iterating keys; destructuring; spread and rest (`...`) for arrays and objects; `JSON.stringify`/`JSON.parse`; `Map` for counting and lookups; `Set` for membership and uniqueness; reference vs value.

**Probe:** objects compared by reference; spread making only a shallow copy; `Map` vs plain object for arbitrary keys; iteration order assumptions.

**Exercises:**
- `08-01-word-frequency` — count words, case-insensitive.
- `08-02-first-unique-char` — index of first non-repeating character.
- `08-03-group-anagrams` — group words that are anagrams.

## 9. TypeScript types: unions, narrowing, null safety

**Learned when:** the Learner models data with type aliases and unions, and narrows `undefined`/`null` and union members safely.

**Teach:** type aliases and interfaces; optional properties; union types; literal types; tuples; narrowing with `typeof`, `in`, and discriminant fields; `undefined` vs `null`; optional chaining (`?.`) and nullish coalescing (`??`); why types catch bugs before running.

**Probe:** using a value before checking it exists; `as` to silence errors; unions treated as intersections; `??` vs `||` with `0` and `""`.

**Exercises:**
- `09-01-shape-area` — area of a discriminated-union shape.
- `09-02-safe-average-score` — average of optional scores, skipping missing ones.
- `09-03-parse-command` — parse a text command into a typed union or an error.

## 10. Higher-order functions and closures

**Learned when:** the Learner rewrites Topic 6 loops with `map`/`filter`/`reduce` and explains what a closure captures.

**Teach:** functions as values; callbacks; `map`, `filter`, `reduce`, `some`, `every`, `find`; returning functions; closures over variables.

**Probe:** forgetting `reduce`'s initial value; `map` used for side effects; a closure capturing a variable that later changes.

**Exercises:**
- `10-01-order-totals` — totals per customer with `reduce`.
- `10-02-make-counter` — a counter factory using a closure.
- `10-03-compose-pipeline` — compose functions left to right.

## 11. Generics and utility types

**Learned when:** the Learner writes a generic function that keeps its caller's types, and uses `Partial`, `Pick`, `Omit` and `Record` instead of copying type definitions.

**Teach:** why `any` loses information; type parameters on functions (`<T>`); inference of type arguments; constraints (`extends`, `keyof`); generic types for arrays and records; utility types `Partial`, `Pick`, `Omit`, `Record`, `Readonly`.

**Probe:** reaching for `any` instead of a type parameter; a type parameter used only once (adds nothing); believing generics exist at runtime.

**Exercises:**
- `11-01-last-and-chunk` — generic `last` and `chunk` that keep the element type.
- `11-02-group-by` — generic `groupBy` with a key function.
- `11-03-pick-and-patch` — `pick` with `keyof` and a non-mutating `applyPatch` with `Partial`.

## 12. Recursion

**Learned when:** the Learner names the base case and the smaller subproblem before writing a recursive function, and traces the call stack.

**Teach:** base case; recursive case making progress; the call stack; recursion on arrays, strings and nested data; when a loop is clearer.

**Probe:** missing base case; recursion that doesn't shrink the input; confusing returning with printing inside recursion.

**Exercises:**
- `12-01-power` — `base ** exp` without `**`, using halving.
- `12-02-flatten-nested` — flatten arbitrarily nested number arrays.
- `12-03-permutations` — all permutations of a short string.

## 13. Errors and input validation

**Learned when:** the Learner decides where to validate, throws meaningful errors, handles them at the right level, and turns `unknown` input into a typed value safely.

**Teach:** `throw`, `try`/`catch`/`finally`; `Error` messages; validating at boundaries; `unknown` vs `any` for untrusted input; type predicates (`value is T`); returning a result object vs throwing; never swallowing errors silently.

**Probe:** catching everything and continuing; validating deep inside instead of at the entry point; error messages without context; `as` on unvalidated data.

**Exercises:**
- `13-01-parse-age` — parse an age string or throw a descriptive error.
- `13-02-safe-divide-result` — return `{ ok, value }` or `{ ok, error }`.
- `13-03-validate-signup` — collect all validation errors for a signup form.

## 14. Promises, async/await and the event loop

**Learned when:** the Learner predicts the order of log output for mixed sync/async code using the event loop, and runs async work sequentially or in parallel on purpose.

**Teach:** why async exists; the event loop: call stack, task queue, microtask queue (promise callbacks run before timers); promises and their states; `async`/`await`; `try`/`catch` with await; `Promise.all`; sequential vs parallel; timeouts. (Node's event loop phases in depth come in Phase 3.)

**Probe:** forgetting `await`; `await` inside `forEach`; assuming `Promise.all` stops other work when one fails; expecting `setTimeout(fn, 0)` to run before a resolved promise's `then`.

**Exercises:**
- `14-01-retry` — retry an async function up to n times.
- `14-02-fetch-all-in-order` — run tasks in parallel, return results in input order.
- `14-03-with-timeout` — reject if a promise takes too long.

## 15. Reading and debugging code

**Learned when:** the Learner finds a bug by forming a hypothesis and checking it (reading the error, tracing, logging), not by random edits.

**Teach:** reading error messages and stack traces; reproducing a bug; tracing with a table; targeted logging; reading unfamiliar code top-down; minimal fixes.

**Probe:** changing several things at once; fixing the symptom instead of the cause; not re-running tests after a fix.

**Exercises:** (the starter contains buggy code; the Learner fixes it)
- `15-01-debug-average` — an average function with two bugs.
- `15-02-debug-binary-to-decimal` — a binary-string converter with an off-by-one.
- `15-03-debug-dedupe` — a dedupe that mutates while iterating.
