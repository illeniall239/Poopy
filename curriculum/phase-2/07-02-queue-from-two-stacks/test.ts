import { test } from "node:test";
import assert from "node:assert/strict";
import { TwoStackQueue } from "./solution.ts";

test("values come out in the order they went in", () => {
  const q = new TwoStackQueue<number>();
  q.enqueue(1);
  q.enqueue(2);
  q.enqueue(3);
  assert.deepEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3]);
});

test("peek returns the front without removing it", () => {
  const q = new TwoStackQueue<string>();
  q.enqueue("a");
  q.enqueue("b");
  assert.deepEqual([q.peek(), q.peek(), q.size(), q.dequeue()], ["a", "a", 2, "a"]);
});

test("mixed enqueues and dequeues keep FIFO order", () => {
  const q = new TwoStackQueue<number>();
  q.enqueue(1);
  q.enqueue(2);
  const first = q.dequeue();
  q.enqueue(3);
  q.enqueue(4);
  const second = q.dequeue();
  q.enqueue(5);
  assert.deepEqual([first, second, q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3, 4, 5]);
});

test("empty queue returns undefined and size 0", () => {
  const q = new TwoStackQueue<number>();
  assert.deepEqual([q.size(), q.dequeue(), q.peek(), q.size()], [0, undefined, undefined, 0]);
});

test("size counts values on both sides", () => {
  const q = new TwoStackQueue<number>();
  q.enqueue(1);
  q.enqueue(2);
  q.dequeue();
  q.enqueue(3);
  q.enqueue(4);
  assert.equal(q.size(), 3);
});

test("dequeue on an empty queue changes nothing", () => {
  const q = new TwoStackQueue<number>();
  q.dequeue();
  q.enqueue(7);
  assert.deepEqual([q.size(), q.dequeue(), q.size()], [1, 7, 0]);
});

test("separate queues don't share values", () => {
  const a = new TwoStackQueue<number>();
  const b = new TwoStackQueue<number>();
  a.enqueue(1);
  b.enqueue(2);
  assert.deepEqual([a.dequeue(), b.dequeue(), a.size(), b.size()], [1, 2, 0, 0]);
});

test("200000 values with 200000 mixed calls, amortized O(1)", () => {
  const n = 200000;
  const q = new TwoStackQueue<number>();
  for (let i = 0; i < n; i++) q.enqueue(i);
  let wrong = 0;
  for (let i = 0; i < n; i++) {
    if (q.peek() !== i) wrong++;
    if (q.dequeue() !== i) wrong++;
    q.enqueue(n + i);
  }
  assert.equal(wrong, 0);
  assert.equal(q.size(), n);
  assert.equal(q.peek(), n);
});
