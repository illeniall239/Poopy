import { test } from "node:test";
import assert from "node:assert/strict";
import { TreeNode, isValidBst } from "./solution.ts";

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

// Level-order values of a balanced BST holding 0..n-1; for n = 2^h - 1 the tree is complete.
function balancedBstLevelOrder(n: number): number[] {
  const values: number[] = [];
  const ranges: [number, number][] = [[0, n]];
  for (let head = 0; head < ranges.length; head++) {
    const [lo, hi] = ranges[head];
    if (lo >= hi) continue;
    const mid = (lo + hi) >> 1;
    values.push(mid);
    ranges.push([lo, mid], [mid + 1, hi]);
  }
  return values;
}

test("small valid tree", () => {
  assert.equal(isValidBst(fromLevelOrder([2, 1, 3])), true);
});

test("right child smaller than root", () => {
  assert.equal(isValidBst(fromLevelOrder([5, 1, 4, null, null, 3, 6])), false);
});

test("grandchild breaks an ancestor's bound", () => {
  assert.equal(isValidBst(fromLevelOrder([5, 4, 6, null, null, 3, 7])), false);
});

test("equal values are not allowed", () => {
  assert.equal(isValidBst(fromLevelOrder([2, 2, 2])), false);
  assert.equal(isValidBst(fromLevelOrder([2, 1, 2])), false);
});

test("empty tree and single node are valid", () => {
  assert.equal(isValidBst(null), true);
  assert.equal(isValidBst(fromLevelOrder([7])), true);
});

test("extreme 32-bit values are still valid", () => {
  assert.equal(isValidBst(fromLevelOrder([-2147483648, null, 2147483647])), true);
  assert.equal(isValidBst(fromLevelOrder([2147483647, -2147483648])), true);
});

test("left descendant larger than the root", () => {
  assert.equal(isValidBst(fromLevelOrder([3, 1, 5, 0, 2, 4, 6])), true);
  assert.equal(isValidBst(fromLevelOrder([3, 1, 5, 0, 4, 2, 6])), false);
});

test("balanced valid tree of 131071 nodes in O(n)", () => {
  assert.equal(isValidBst(fromLevelOrder(balancedBstLevelOrder(131071))), true);
});

test("balanced tree of 131071 nodes with one deep node out of place", () => {
  const values = balancedBstLevelOrder(131071);
  values[values.length - 2] = -1; // still smaller than its parent, but it sits in the root's right subtree
  assert.equal(isValidBst(fromLevelOrder(values)), false);
});
