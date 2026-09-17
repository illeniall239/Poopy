import java.util.List;

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

    /** One list per level, top to bottom, each left to right; an empty list for an empty tree. */
    public static List<List<Integer>> valuesByLevel(TreeNode root) {
        throw new UnsupportedOperationException("Not implemented");
    }
}
