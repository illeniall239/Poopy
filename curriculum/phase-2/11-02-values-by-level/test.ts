import { test } from "node:test";
import assert from "node:assert/strict";
import { TreeNode, valuesByLevel } from "./solution.ts";

// Builds a tree from a level-order array; null marks a missing child.
function fromLevelOrder(values: (number | null)[]): TreeNode | null {
  if (values.length === 0 || values[0] === null) return null;
  const root = new TreeNode(values[0]);
  const queue = [root];
  let head = 0;
  let i = 1;
  while (i < values.length) {
    const node = queue[head++];
    const left = values[i++];
    if (left != null) queue.push((node.left = new TreeNode(left)));
    if (i < values.length) {
      const right = values[i++];
      if (right != null) queue.push((node.right = new TreeNode(right)));
    }
  }
  return root;
}

function completeTree(n: number): TreeNode | null {
  return fromLevelOrder(Array.from({ length: n }, (_, i) => i));
}

test("three levels", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([3, 9, 20, null, null, 15, 7])), [[3], [9, 20], [15, 7]]);
});

test("chain with one node per level", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([1, null, 2, 3])), [[1], [2], [3]]);
});

test("single node", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([1])), [[1]]);
});

test("empty tree", () => {
  assert.deepEqual(valuesByLevel(null), []);
});

test("missing children leave no gaps", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([1, 2, 3, null, 4, 5, null, 6, null, null, 7])), [[1], [2, 3], [4, 5], [6, 7]]);
});

test("left to right within a level", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([10, 5, 15, 3, 7, 12, 20])), [[10], [5, 15], [3, 7, 12, 20]]);
});

test("repeated values are each listed", () => {
  assert.deepEqual(valuesByLevel(fromLevelOrder([1, 1, 1, null, 1])), [[1], [1, 1], [1]]);
});

test("balanced tree of 131071 nodes in O(n)", () => {
  const levels = valuesByLevel(completeTree(131071));
  assert.equal(levels.length, 17);
  for (let d = 0; d < 17; d++) {
    const start = 2 ** d - 1;
    assert.deepEqual(levels[d], Array.from({ length: 2 ** d }, (_, i) => start + i));
  }
});
