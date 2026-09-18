// Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
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

export function valuesByLevel(root: TreeNode | null): number[][] {
  const levels: number[][] = [];
  if (root === null) return levels;
  let current: TreeNode[] = [root];
  while (current.length > 0) {
    const next: TreeNode[] = [];
    const values: number[] = [];
    for (const node of current) {
      values.push(node.val);
      if (node.left !== null) next.push(node.left);
      if (node.right !== null) next.push(node.right);
    }
    levels.push(values);
    current = next;
  }
  return levels;
}
