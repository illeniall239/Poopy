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
        check("three levels", () -> Solution.valuesByLevel(fromLevelOrder(3, 9, 20, null, null, 15, 7)),
                List.of(List.of(3), List.of(9, 20), List.of(15, 7)));
        check("chain with one node per level", () -> Solution.valuesByLevel(fromLevelOrder(1, null, 2, 3)),
                List.of(List.of(1), List.of(2), List.of(3)));
        check("single node", () -> Solution.valuesByLevel(fromLevelOrder(1)), List.of(List.of(1)));
        check("empty tree", () -> Solution.valuesByLevel(null), List.of());
        check("missing children leave no gaps",
                () -> Solution.valuesByLevel(fromLevelOrder(1, 2, 3, null, 4, 5, null, 6, null, null, 7)),
                List.of(List.of(1), List.of(2, 3), List.of(4, 5), List.of(6, 7)));
        check("left to right within a level", () -> Solution.valuesByLevel(fromLevelOrder(10, 5, 15, 3, 7, 12, 20)),
                List.of(List.of(10), List.of(5, 15), List.of(3, 7, 12, 20)));
        check("repeated values are each listed", () -> Solution.valuesByLevel(fromLevelOrder(1, 1, 1, null, 1)),
                List.of(List.of(1), List.of(1, 1), List.of(1)));
        check("balanced tree of 131071 nodes in O(n)", () -> {
            List<List<Integer>> levels = Solution.valuesByLevel(completeTree(131071));
            if (levels.size() != 17) return false;
            for (int d = 0; d < 17; d++) {
                List<Integer> expected = new ArrayList<>();
                for (int i = 0; i < (1 << d); i++) expected.add((1 << d) - 1 + i);
                if (!levels.get(d).equals(expected)) return false;
            }
            return true;
        }, true);

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}
