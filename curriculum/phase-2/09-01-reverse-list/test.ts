import { test } from "node:test";
import assert from "node:assert/strict";
import { ListNode, reverseList } from "./solution.ts";

function nodesOf(values: number[]): ListNode[] {
  const nodes = values.map((v) => new ListNode(v));
  for (let i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
  return nodes;
}

function fromArray(values: number[]): ListNode | null {
  return nodesOf(values)[0] ?? null;
}

// Walks at most `limit` nodes so a list that accidentally loops can't hang the test.
function toArray(head: ListNode | null, limit = 2000000): number[] {
  const values: number[] = [];
  for (let node = head; node !== null && values.length < limit; node = node.next) values.push(node.val);
  return values;
}

test("reverses five nodes", () => {
  assert.deepEqual(toArray(reverseList(fromArray([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1]);
});

test("reverses two nodes", () => {
  assert.deepEqual(toArray(reverseList(fromArray([1, 2]))), [2, 1]);
});

test("one node returns the same node", () => {
  const node = new ListNode(7);
  const result = reverseList(node);
  assert.equal(result, node);
  assert.equal(node.next, null);
});

test("empty list returns null", () => {
  assert.equal(reverseList(null), null);
});

test("repeated values", () => {
  assert.deepEqual(toArray(reverseList(fromArray([1, 1, 2, 3, 3]))), [3, 3, 2, 1, 1]);
});

test("reuses the original nodes and ends at the old head", () => {
  const nodes = nodesOf([10, 20, 30, 40]);
  let node = reverseList(nodes[0]);
  const seen: ListNode[] = [];
  while (node !== null && seen.length < 10) {
    seen.push(node);
    node = node.next;
  }
  assert.equal(seen.length, 4);
  assert.ok(seen.every((n, i) => n === nodes[3 - i]), "expected the same node objects in reverse order");
  assert.equal(nodes[0].next, null);
});

test("200000 nodes without recursion in O(n)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => i);
  const result = toArray(reverseList(fromArray(values)), n + 1);
  assert.equal(result.length, n);
  assert.ok(result.every((v, i) => v === n - 1 - i), "values are not in reverse order");
});
