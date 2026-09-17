// Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
export class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;

  constructor(val: number, left: TreeNode | null = null, right: TreeNode | null = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function inRange(node: TreeNode | null, low: number, high: number): boolean {
  if (node === null) return true;
  if (node.val <= low || node.val >= high) return false;
  return inRange(node.left, low, node.val) && inRange(node.right, node.val, high);
}

export function isValidBst(root: TreeNode | null): boolean {
  return inRange(root, -Infinity, Infinity);
}
