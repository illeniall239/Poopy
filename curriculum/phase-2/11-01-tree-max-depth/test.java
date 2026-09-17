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

    static Solution.TreeNode completeTree(int n) {
        Integer[] values = new Integer[n];
        for (int i = 0; i < n; i++) values[i] = i;
        return fromLevelOrder(values);
    }

    public static void main(String[] args) {
        check("three levels", () -> Solution.maxDepth(fromLevelOrder(3, 9, 20, null, null, 15, 7)), 3);
        check("only a right child", () -> Solution.maxDepth(fromLevelOrder(1, null, 2)), 2);
        check("single node", () -> Solution.maxDepth(fromLevelOrder(1)), 1);
        check("empty tree", () -> Solution.maxDepth(null), 0);
        check("left-leaning chain", () -> Solution.maxDepth(fromLevelOrder(1, 2, null, 3, null, 4)), 4);
        check("deeper on one side", () -> Solution.maxDepth(fromLevelOrder(1, 2, 3, 4, null, null, null, 5, null, 6)), 5);
        check("values do not matter", () -> Solution.maxDepth(fromLevelOrder(-7, -7, -7, 0, 0)), 3);
        check("balanced tree of 131071 nodes in O(n)", () -> Solution.maxDepth(completeTree(131071)), 17);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
