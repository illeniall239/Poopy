import { test } from "node:test";
import assert from "node:assert/strict";
import { TreeNode, maxDepth } from "./solution.ts";

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
  assert.equal(maxDepth(fromLevelOrder([3, 9, 20, null, null, 15, 7])), 3);
});

test("only a right child", () => {
  assert.equal(maxDepth(fromLevelOrder([1, null, 2])), 2);
});

test("single node", () => {
  assert.equal(maxDepth(fromLevelOrder([1])), 1);
});

test("empty tree", () => {
  assert.equal(maxDepth(null), 0);
});

test("left-leaning chain", () => {
  assert.equal(maxDepth(fromLevelOrder([1, 2, null, 3, null, 4])), 4);
});

test("deeper on one side", () => {
  assert.equal(maxDepth(fromLevelOrder([1, 2, 3, 4, null, null, null, 5, null, 6])), 5);
});

test("values do not matter", () => {
  assert.equal(maxDepth(fromLevelOrder([-7, -7, -7, 0, 0])), 3);
});

test("balanced tree of 131071 nodes in O(n)", () => {
  assert.equal(maxDepth(completeTree(131071)), 17);
});
