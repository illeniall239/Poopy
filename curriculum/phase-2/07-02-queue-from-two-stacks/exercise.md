# Queue from two stacks

Topic: 7. Stacks and queues
Difficulty: 2 of 3

## Problem

A print server handles jobs in the order they arrive. You only have stacks to build it with.

Write a generic class `TwoStackQueue<T>` with these methods:

- `enqueue(value: T): void` adds `value` to the back of the queue.
- `dequeue(): T | undefined` removes and returns the value at the front. On an empty queue it returns `undefined` and changes nothing.
- `peek(): T | undefined` returns the value at the front without removing it, or `undefined` when the queue is empty.
- `size(): number` returns how many values are in the queue.

Values come out in exactly the order they went in, however enqueues and dequeues are mixed. Separate queues never share values.

Store the values in two arrays that you use only as stacks: `push`, `pop`, `length` and reading the last element. Don't use `shift`, `unshift`, `splice` or indexing from the front.

## Examples

```
const q = new TwoStackQueue<number>();
q.enqueue(1); q.enqueue(2);
q.peek()     → 1
q.dequeue()  → 1
q.enqueue(3);
q.size()     → 2
q.dequeue()  → 2
q.dequeue()  → 3
q.dequeue()  → undefined
```

## Constraints

- Up to 600000 method calls on one queue.
- Required: every method is amortized O(1): any sequence of m calls takes O(m) time in total.
- The large test keeps 200000 values in the queue while mixing 200000 dequeues and enqueues, so moving every value from one stack to the other on each call is too slow.

## Hints

1. If you push 1, 2, 3 onto one stack and then pop everything onto a second stack, in what order are they sitting on the second stack?
2. Give each stack a job: one for arriving values, one for leaving values. Which stack should `dequeue` look at first?
3. When exactly do you need to move values from the arriving stack to the leaving stack? What goes wrong if you move them while the leaving stack still has values in it?
4. A single value can be moved from one stack to the other at most how many times in its whole life? What does that tell you about the total work for m calls?

## Explain-back

- Why does using an array's `shift` for `dequeue` make processing n jobs O(n²) in general, even though each call looks like one line?
- Walk through `enqueue(1)`, `enqueue(2)`, `dequeue()`, `enqueue(3)`, `dequeue()`, `dequeue()`, showing both stacks after each call.
- One `dequeue` in your class can take O(n) time. Why is it still correct to call the class amortized O(1) per call?
- What is the space complexity of the queue, and does moving values between stacks ever duplicate them?
