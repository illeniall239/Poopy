public class Solution {
    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    /** True if every node is greater than all of its left subtree and less than all of its right subtree. */
    public static boolean isValidBst(TreeNode root) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
