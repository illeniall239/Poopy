import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.Supplier;

public class SolutionTest {
    static int passed = 0, failed = 0;

    static void check(String name, Supplier<Object> got, Object expected) {
        Object value;
        try {
            value = got.get();
        } catch (Throwable e) {
            failed++;
            System.out.println("FAIL - " + name + "\n    threw: " + e);
            return;
        }
        if (Objects.deepEquals(value, expected)) {
            passed++;
            System.out.println("ok - " + name);
        } else {
            failed++;
            System.out.println("FAIL - " + name + "\n    expected: " + expected + "\n    got:      " + value);
        }
    }

    /** Builds a tree from a level-order array; null marks a missing child. */
    static Solution.TreeNode fromLevelOrder(Integer... values) {
        if (values.length == 0 || values[0] == null) return null;
        Solution.TreeNode root = new Solution.TreeNode(values[0]);
        List<Solution.TreeNode> queue = new ArrayList<>();
        queue.add(root);
        int head = 0, i = 1;
        while (i < values.length) {
            Solution.TreeNode node = queue.get(head++);
            Integer left = values[i++];
            if (left != null) queue.add(node.left = new Solution.TreeNode(left));
            if (i < values.length) {
                Integer right = values[i++];
                if (right != null) queue.add(node.right = new Solution.TreeNode(right));
            }
        }
        return root;
    }

    /** Level-order values of a balanced BST holding 0..n-1; for n = 2^h - 1 the tree is complete. */
    static Integer[] balancedBstLevelOrder(int n) {
        List<Integer> values = new ArrayList<>();
        List<int[]> ranges = new ArrayList<>();
        ranges.add(new int[] {0, n});
        for (int head = 0; head < ranges.size(); head++) {
            int lo = ranges.get(head)[0], hi = ranges.get(head)[1];
            if (lo >= hi) continue;
            int mid = (lo + hi) >>> 1;
            values.add(mid);
            ranges.add(new int[] {lo, mid});
            ranges.add(new int[] {mid + 1, hi});
        }
        return values.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        check("small valid tree", () -> Solution.isValidBst(fromLevelOrder(2, 1, 3)), true);
        check("right child smaller than root", () -> Solution.isValidBst(fromLevelOrder(5, 1, 4, null, null, 3, 6)), false);
        check("grandchild breaks an ancestor's bound", () -> Solution.isValidBst(fromLevelOrder(5, 4, 6, null, null, 3, 7)), false);
        check("equal values are not allowed",
                () -> List.of(Solution.isValidBst(fromLevelOrder(2, 2, 2)), Solution.isValidBst(fromLevelOrder(2, 1, 2))),
                List.of(false, false));
        check("empty tree and single node are valid",
                () -> List.of(Solution.isValidBst(null), Solution.isValidBst(fromLevelOrder(7))), List.of(true, true));
        check("extreme 32-bit values are still valid", () -> List.of(
                Solution.isValidBst(fromLevelOrder(Integer.MIN_VALUE, null, Integer.MAX_VALUE)),
                Solution.isValidBst(fromLevelOrder(Integer.MAX_VALUE, Integer.MIN_VALUE))), List.of(true, true));
        check("left descendant larger than the root", () -> List.of(
                Solution.isValidBst(fromLevelOrder(3, 1, 5, 0, 2, 4, 6)),
                Solution.isValidBst(fromLevelOrder(3, 1, 5, 0, 4, 2, 6))), List.of(true, false));
        check("balanced valid tree of 131071 nodes in O(n)",
                () -> Solution.isValidBst(fromLevelOrder(balancedBstLevelOrder(131071))), true);
        check("balanced tree of 131071 nodes with one deep node out of place", () -> {
            Integer[] values = balancedBstLevelOrder(131071);
            values[values.length - 2] = -1; // still smaller than its parent, but it sits in the root's right subtree
            return Solution.isValidBst(fromLevelOrder(values));
        }, false);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
