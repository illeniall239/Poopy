# Phase 2 — Data structures and algorithms

71 hours over about 4 weeks, 17 Topics. For a Learner who has finished Phase 1 (TypeScript fundamentals, recursion, generics, `Map`/`Set`) and is preparing for junior full-stack interviews.

Every Topic below lists:
- **Learned when** — what the Learner must show, on top of the standard rule (Exercises pass without hints, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Exercises** — folder names under this directory, in order.

Exercise folder layout: `exercise.md` (problem, examples, constraints including the required time and space complexity, Hint Ladder, and the questions the Breakdown answers), then per language a starter, a test and a reference: `starter.ts`/`test.ts`/`reference.ts` (TypeScript; JavaScript is derived from it), `starter.py`/`test.py`/`reference.py`, `starter.java`/`test.java`/`reference.java`. Where a complexity is required, the test includes a large input that a slower solution cannot finish in time. Node types the problem needs (list nodes, tree nodes) are defined in the starter. The reference is only used by `scripts/verify-exercises.mjs` to prove the tests are correct; it is shown in the Breakdown once the Learner's own solution passes. The problem text is written in TypeScript terms; the Tutor translates for other languages.

---

## 1. How computers run code

**Learned when:** the Learner explains, for a small program, where each value lives (stack or heap), why deep recursion overflows, and what happens between saving a `.ts` file and the CPU running instructions.

**Teach:** the CPU fetch–decode–execute cycle; memory as numbered bytes; numbers in binary and why a 32-bit integer has a fixed range; the call stack: one frame per call holding parameters and locals, popped on return; the heap for objects and arrays, reached through references; garbage collection freeing unreachable objects; processes (own memory) vs threads (shared memory); compiled vs interpreted vs JIT; how a JavaScript engine runs code: parse, bytecode, hot code optimized by the JIT; JavaScript's single thread plus the event loop (from Phase 1); cache locality: why arrays of contiguous values are fast to scan.

**Probe:** believing variables hold objects rather than references to them; thinking the stack and heap are the data structures of the same name; stack overflow blamed on "too much memory" rather than too many frames; assuming JavaScript runs on several threads; "interpreted means slow, compiled means fast" with no nuance about JIT.

**Exercises:**
- `01-01-to-base` — convert a non-negative integer to a string in any base 2–16 by repeated division, and back again.
- `01-02-max-call-depth` — given which functions each function calls, simulate running from an entry function and return the deepest call stack, or report infinite recursion.
- `01-03-record-memory-size` — bytes used by a record of typed fields laid out with alignment padding, and by an array of n such records.

## 2. Big-O: time and space complexity

**Learned when:** the Learner states the time and space complexity of their own code and of Phase 1 solutions, and rewrites a quadratic solution as a linear one when a data structure allows it.

**Teach:** counting basic steps as input grows; dropping constants and lower terms; O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) with an example of each; nested loops multiply, sequential loops add; halving gives log n; space complexity: extra memory, including the recursion stack; best, worst and average case; amortized cost (array `push`); hidden costs of built-ins (`includes`, `indexOf`, `slice`, `shift`, spread and string concatenation in a loop are O(n)); rough speed budget: about 10⁸ simple steps per second, so n = 10⁵ rules out O(n²).

**Probe:** calling any loop O(n) even when its body is O(n); forgetting that `arr.includes` inside a loop is quadratic; ignoring recursion stack in space complexity; thinking O(2n) is slower than O(n) in Big-O terms; counting input size as extra space.

**Exercises:**
- `02-01-has-duplicate` — does an array contain any repeated value, in O(n) time.
- `02-02-range-sum-queries` — answer many "sum from index i to j" queries in O(n + q) using prefix sums.
- `02-03-rotate-in-place` — rotate an array right by k steps in O(n) time and O(1) extra space, with k possibly much larger than n.

## 3. Classes for building data structures

**Learned when:** the Learner builds a small data structure as a class that hides its internal storage, keeps its invariants true after every method, and states each method's complexity.

**Teach:** `class`, `constructor`, fields and methods; `private` and `readonly`; `this` refers to the instance the method was called on; generic classes (`class Stack<T>`); an invariant the class guarantees; a dynamic array grows by doubling, so `push` is amortized O(1); a hash map: hashing a key to a bucket index, collisions handled by chaining, load factor and resizing, O(1) average and O(n) worst case; exposing a small public API.

**Probe:** a method passed as a callback losing `this`; exposing internal arrays so callers break the invariant; growing capacity by +1 instead of doubling (quadratic total); forgetting to rehash every entry when resizing; assuming hash map operations are O(1) in the worst case.

**Exercises:**
- `03-01-dynamic-array` — a growable array class on top of fixed-capacity storage that doubles when full.
- `03-02-hash-map-chaining` — a string-keyed hash map with buckets, collision chaining and resizing past a load factor.
- `03-03-sparse-matrix` — store only non-zero cells and multiply the matrix by a vector in time proportional to the non-zero count.

## 4. Arrays and hashing

**Learned when:** the Learner reaches for a `Map` or `Set` to turn repeated searching into O(1) lookups, and explains the time/space trade-off.

**Teach:** array access O(1), insert/delete in the middle O(n); `Set` for "have I seen this?"; `Map` for counts and value → index; storing what you need while scanning once; frequency counting; bucket sort when values are bounded (counts ≤ n); building a canonical key (sorted string, counts tuple) for grouping; trading O(n) extra space for O(n) time.

**Probe:** checking the map after inserting the current element (pairing an element with itself); sorting when hashing would give O(n); using an object with non-string keys; assuming `Map` iteration order means sorted order.

**Exercises:**
- `04-01-pair-with-target-sum` — indices of two different elements adding to a target, in one pass.
- `04-02-top-k-frequent` — the k most frequent values in better than O(n log n).
- `04-03-longest-consecutive-run` — length of the longest run of consecutive integers in an unsorted array, in O(n).

## 5. Two pointers

**Learned when:** the Learner recognizes when a sorted array or a symmetric structure lets two indices replace a nested loop, and argues why moving a pointer never skips an answer.

**Teach:** pointers from both ends moving inward; pointers moving in the same direction (read/write); why sortedness lets you discard one side; sorting first costs O(n log n); skipping duplicates to avoid repeated answers; O(1) extra space; reducing a three-element problem to a two-element one with an outer loop (O(n²)).

**Probe:** using two pointers on unsorted input; moving both pointers when only one should move; skipping duplicates in the wrong place, losing or repeating triplets; loop condition `<=` letting both pointers use the same element.

**Exercises:**
- `05-01-sorted-pair-sum` — find two values in a sorted array summing to a target with O(1) extra space.
- `05-02-zero-sum-triplets` — all unique triplets that sum to zero, without duplicate triplets.
- `05-03-widest-container` — the largest area of water held between two walls from an array of wall heights, in O(n).

## 6. Sliding window

**Learned when:** the Learner solves a "best contiguous subarray/substring" problem with a window that grows and shrinks, and explains why the total work is O(n) despite the inner loop.

**Teach:** fixed-size window: add the entering element, remove the leaving one; variable-size window: expand right, shrink left while the window is invalid; keeping window state in counters or a `Map`; each index enters and leaves once, so O(n) total; when the answer is recorded (after shrinking vs before); O(k) space for the character counts.

**Probe:** recomputing the whole window each step (O(n·k)); off-by-one window length (`right - left` vs `right - left + 1`); forgetting to decrement or delete counts when shrinking; calling the nested `while` O(n²).

**Exercises:**
- `06-01-max-sum-fixed-window` — the largest sum of any k consecutive elements.
- `06-02-longest-unique-substring` — length of the longest substring with no repeated character.
- `06-03-smallest-covering-window` — the shortest substring of s containing every character of t, counting repeats.

## 7. Stacks and queues

**Learned when:** the Learner chooses a stack for "most recent unmatched thing" problems and a queue for first-in-first-out work, and implements a queue with O(1) operations without `shift`.

**Teach:** stack push/pop O(1) on an array's end; LIFO for matching and undo; queue FIFO; `shift` is O(n) in JavaScript, so queues use a head index or two stacks; amortized O(1) for the two-stack queue; monotonic stack: keep elements in decreasing order to find the next greater element in O(n).

**Probe:** popping an empty stack; using `shift` in a loop and getting O(n²); returning true for brackets when the stack still has items at the end; thinking the monotonic stack's inner `while` makes it O(n²).

**Exercises:**
- `07-01-balanced-brackets` — are `()[]{}` brackets correctly nested.
- `07-02-queue-from-two-stacks` — a queue class with amortized O(1) enqueue, dequeue and peek using only two stacks.
- `07-03-days-until-warmer` — for each day, how many days until a warmer temperature, in O(n).

## 8. Binary search

**Learned when:** the Learner writes binary search with a stated loop invariant, gets the bounds right first time, and applies it to searching over possible answers.

**Teach:** halving the search space gives O(log n); `lo`, `hi` and what each boundary means (inclusive vs exclusive); computing `mid` without overflow (`lo + (hi - lo) / 2` in Java); the loop invariant; finding the first index where a condition becomes true; rotated sorted arrays: one half is always sorted; binary search on the answer when a check is monotonic.

**Probe:** off-by-one in bounds (`hi = mid` vs `hi = mid - 1` mixed with `<` vs `<=`); infinite loop when `mid` never moves `lo`; integer overflow of `lo + hi` in Java; binary searching unsorted data; forgetting the "not found" return.

**Exercises:**
- `08-01-binary-search-index` — index of a target in a sorted array or -1, in O(log n).
- `08-02-search-rotated-sorted` — find a target in a sorted array that has been rotated, in O(log n).
- `08-03-slowest-finishing-speed` — the smallest eating speed that finishes all piles within h hours.

## 9. Linked lists

**Learned when:** the Learner manipulates `next` pointers on paper before coding, uses a dummy head to avoid special cases, and uses fast and slow pointers for middle and cycle problems.

**Teach:** nodes and `next` references; access O(n), insert/delete at a known node O(1); traversal until `null`; reversing with `prev`/`curr`/`next`; dummy (sentinel) head; fast and slow pointers: middle of a list, cycle detection in O(1) space; doubly linked lists for O(1) removal; combining a hash map with a doubly linked list.

**Probe:** losing the rest of the list by overwriting `next` before saving it; not handling empty or one-node lists; fast pointer checking `fast.next` without checking `fast`; using a `Set` of visited nodes when O(1) space was required; forgetting to update both `prev` and `next` in a doubly linked list.

**Exercises:**
- `09-01-reverse-list` — reverse a singly linked list iteratively in O(1) extra space.
- `09-02-middle-and-cycle` — find the middle node, and detect whether a list loops, both with fast and slow pointers.
- `09-03-lru-cache` — a least-recently-used cache class with O(1) get and put, built from a hash map and a doubly linked list.

## 10. Sorting

**Learned when:** the Learner implements merge sort and quicksort, states their time and space complexity and stability, and uses the built-in sort with a correct comparator when that is enough.

**Teach:** why O(n²) sorts fail at n = 10⁵; merge sort: split, sort halves, merge; O(n log n) always, O(n) extra space, stable; quicksort: partition around a pivot; O(n log n) average, O(n²) worst case on bad pivots; random pivot and handling many equal values; in-place with O(log n) stack; stability and why it matters for multi-key sorts; the built-in sort: O(n log n), stable in modern JavaScript, Python and Java objects; comparators returning negative/zero/positive.

**Probe:** JavaScript's default `sort()` comparing numbers as strings; comparator returning a boolean; quicksort with first-element pivot on already-sorted input; merge that drops the leftover elements of one half; believing you must hand-write sorts in interviews.

**Exercises:**
- `10-01-merge-sort` — sort numbers with merge sort, returning a new array, fast enough for 200 000 elements.
- `10-02-quicksort-in-place` — sort in place with quicksort that stays fast on sorted and all-equal input.
- `10-03-sort-by-several-keys` — order records by one field descending then another ascending using the built-in sort.

## 11. Trees

**Learned when:** the Learner writes tree recursion by deciding what each call returns for its subtree, chooses DFS or BFS for a task, and uses the BST ordering property with bounds.

**Teach:** nodes with `left`/`right`; root, leaf, height; recursive DFS: preorder, inorder, postorder; BFS level by level with a queue; O(n) time, O(h) stack space for DFS, O(width) for BFS; balanced height O(log n) vs degenerate O(n); binary search tree property for every node in a subtree, not just children; inorder traversal of a BST is sorted; BST search/insert O(h).

**Probe:** checking only a node's direct children when validating a BST; forgetting the `null` base case; confusing depth (edges or nodes) at the base case; mixing levels in BFS by not recording the queue size first; assuming every binary tree is a BST or balanced.

**Exercises:**
- `11-01-tree-max-depth` — the number of nodes on the longest root-to-leaf path.
- `11-02-values-by-level` — node values grouped level by level, top to bottom.
- `11-03-validate-bst` — is a binary tree a valid binary search tree.

## 12. Tries

**Learned when:** the Learner builds a trie, explains why prefix lookup costs O(length of the prefix) regardless of how many words are stored, and adapts the search for wildcards.

**Teach:** a node per character with a map of children and an end-of-word flag; insert and search O(L); prefix check vs whole-word check; space O(total characters); collecting all words under a prefix with DFS; branching over all children for a wildcard character; when a `Set` of words is simpler and enough.

**Probe:** treating "path exists" as "word exists" (missing end-of-word flag); storing whole words at every node; thinking trie lookup depends on the number of words; wildcard search that returns after the first child fails instead of trying the others.

**Exercises:**
- `12-01-trie-basics` — a trie class with insert, whole-word search and prefix check.
- `12-02-autocomplete` — the first n stored words in alphabetical order that start with a prefix.
- `12-03-wildcard-word-search` — a word dictionary where `.` in a query matches any single letter.

## 13. Heaps and priority queues

**Learned when:** the Learner implements a binary min-heap on an array, and uses a heap of size k to get "top k" or "merge k" results faster than full sorting.

**Teach:** complete binary tree stored in an array: children at `2i+1`, `2i+2`, parent at `(i-1)/2`; sift up on push, sift down on pop, both O(log n); peek O(1); building from an array; min-heap vs max-heap (negate or flip the comparator); keeping a size-k heap for top k in O(n log k); merging k sorted sequences with a heap of their heads; library heaps: Python `heapq`, Java `PriorityQueue`, none built into JavaScript.

**Probe:** sift down swapping with the wrong child (not the smaller one); thinking a heap array is sorted; using a max-heap for "k largest" and popping n−k times instead of a min-heap of size k; forgetting to move the last element to the root on pop.

**Exercises:**
- `13-01-min-heap` — a min-heap class with push, pop, peek and size, all O(log n) or better.
- `13-02-kth-largest-in-stream` — a class that returns the k-th largest value seen so far after each added number.
- `13-03-merge-k-sorted-arrays` — merge k sorted arrays into one sorted array in O(N log k).

## 14. Backtracking

**Learned when:** the Learner describes the choice tree before coding (choose, explore, un-choose), prunes branches that cannot succeed, and states the exponential complexity.

**Teach:** a decision at each step; the path being built and undoing the last choice; recording a copy of the path at a leaf; include/exclude subsets: O(2ⁿ); controlling duplicates with a start index; pruning when a partial answer is already invalid; permutations O(n!); tracking used columns and diagonals with sets for O(1) checks.

**Probe:** pushing the path itself instead of a copy, so every result ends up empty; forgetting to pop after the recursive call; generating duplicate combinations by restarting from index 0; no pruning, so the search explodes.

**Exercises:**
- `14-01-all-subsets` — every subset of an array of distinct numbers.
- `14-02-combinations-to-target` — all combinations of candidates that sum to a target, each candidate reusable, no duplicate combinations.
- `14-03-count-queen-placements` — the number of ways to place n queens on an n×n board so none attack each other.

## 15. Graphs

**Learned when:** the Learner builds an adjacency list from edges, picks BFS for shortest unweighted paths and DFS for exploring or ordering, and never forgets a visited set.

**Teach:** vertices and edges; directed vs undirected; adjacency list O(V + E) space vs adjacency matrix O(V²); building a `Map` of neighbors from an edge list; BFS with a queue gives shortest paths in unweighted graphs; DFS recursive or with a stack; visited set; O(V + E) traversal; grids as implicit graphs with 4 neighbors and bounds checks; counting connected components; topological order with in-degrees (Kahn's algorithm) and detecting a cycle when not every node is output.

**Probe:** forgetting the visited set (infinite loop on cycles); marking visited when dequeued instead of when enqueued (duplicates in the queue); adding undirected edges in one direction only; grid bounds checked after indexing; using DFS for shortest path.

**Exercises:**
- `15-01-shortest-path-unweighted` — fewest edges between two nodes of an undirected graph given as an edge list, or -1.
- `15-02-count-islands` — the number of connected land regions in a grid.
- `15-03-course-order` — an order to take courses given prerequisite pairs, or an empty array if impossible.

## 16. Dynamic programming

**Learned when:** the Learner defines the state and the recurrence in words, spots overlapping subproblems in a recursion tree, and turns it into a memoized or bottom-up solution with stated complexity.

**Teach:** overlapping subproblems and optimal substructure; the state ("dp[i] means…"); recurrence and base cases; top-down memoization with a `Map` or array; bottom-up tables; time = states × work per state; reducing space to the previous row or last two values; 2-D state for two strings (dp[i][j]); unreachable states (Infinity or -1) in minimization.

**Probe:** recursion without memo re-computing the same subproblem exponentially; a state that does not capture everything needed; wrong base case (`dp[0]`); filling the table in an order that reads cells not yet computed; greedy used where DP is needed (coins 1, 3, 4 for 6).

**Exercises:**
- `16-01-ways-to-climb` — number of distinct ways to climb n steps taking 1 or 2 at a time, in O(n).
- `16-02-fewest-coins` — fewest coins from given denominations to make an amount, or -1.
- `16-03-longest-common-subsequence` — length of the longest subsequence shared by two strings.

## 17. Intervals and greedy algorithms

**Learned when:** the Learner sorts intervals by the right key, argues why a greedy choice is safe (or finds a counterexample), and states O(n log n) from sorting.

**Teach:** intervals as `[start, end]` pairs; overlap test `a.start <= b.end && b.start <= a.end`; sorting by start to merge; sorting by end to keep the most non-overlapping intervals; greedy: make the locally best choice and never revisit; exchange argument, informally; testing a greedy idea against small counterexamples; tracking the farthest reachable index in O(n).

**Probe:** merging without sorting first; open vs closed endpoints (does `[1,2]` overlap `[2,3]`?); sorting by start when the greedy needs end; trusting a greedy rule because it works on the given examples; mutating the input intervals.

**Exercises:**
- `17-01-merge-intervals` — merge all overlapping intervals.
- `17-02-fewest-removals-no-overlap` — the fewest intervals to remove so the rest don't overlap.
- `17-03-can-reach-last-index` — given maximum jump lengths per index, can you reach the last index, in O(n).
